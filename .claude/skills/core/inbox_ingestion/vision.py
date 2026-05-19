"""Claude Vision API interaction for image analysis."""

import base64
import io
import json
import re
from dataclasses import dataclass
from pathlib import Path

import anthropic
from PIL import Image

from .config import ANTHROPIC_API_KEY, VISION_MODEL

MAX_IMAGE_DIMENSION = 7500  # Anthropic limit is 8000; headroom for safety
PIL_FORMAT_TO_MIME = {
    "PNG": "image/png",
    "JPEG": "image/jpeg",
    "GIF": "image/gif",
    "WEBP": "image/webp",
    "BMP": "image/png",   # convert
    "TIFF": "image/png",  # convert
}

VISION_PROMPT = """\
Analyze this image and return a JSON object with exactly these fields:

1. "extracted_text": All visible text in the image, transcribed verbatim. If no text is visible, return an empty string.
2. "description": A 1-2 sentence description of what this image contains (e.g., "Screenshot of a Slack conversation about deployment timelines" or "iPhone photo of a whiteboard with system architecture diagram").
3. "tags": An array of 2-4 categorical tags in kebab-case (e.g., ["slack-chat", "deployment", "team-discussion"]).
4. "slug": A descriptive kebab-case filename slug, max 60 characters (e.g., "slack-deploy-timeline-discussion").
5. "research_targets": An array of external entities worth researching. Each target is an object with:
   - "type": one of "url", "social_handle", "person", "brand", "product", "article"
   - "value": the identifier (e.g., "https://...", "@futurewalt", "Nicolas Boucher", "Claude Code")
   - "context": optional 3-8 word hint to disambiguate (e.g., "AI finance educator", "iOS shortcuts app")
   Return [] if the image is purely personal (private chat, family photo, handwritten note with no external references).
   Otherwise return 1-4 targets. Prefer specific identifiers (handles, URLs, exact names) over generic ones.

Return ONLY the JSON object, no markdown fencing or commentary."""


@dataclass
class ResearchTarget:
    type: str
    value: str
    context: str = ""


@dataclass
class VisionResult:
    extracted_text: str
    description: str
    tags: list[str]
    slug: str
    research_targets: list[ResearchTarget] = None

    def __post_init__(self):
        if self.research_targets is None:
            self.research_targets = []


def prepare_image(image_path: Path) -> tuple[str, str]:
    """Open an image with Pillow, detect actual format, downscale if oversized.

    Returns (base64_data, media_type) ready for the Anthropic API.
    Always re-encodes through Pillow so file-extension lies don't reach the API.
    """
    with Image.open(image_path) as img:
        actual_format = img.format or "PNG"
        target_format = "PNG" if actual_format not in PIL_FORMAT_TO_MIME else actual_format
        if target_format in ("BMP", "TIFF"):
            target_format = "PNG"

        max_dim = max(img.width, img.height)
        if max_dim > MAX_IMAGE_DIMENSION:
            scale = MAX_IMAGE_DIMENSION / max_dim
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size, Image.LANCZOS)

        if target_format == "JPEG" and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        buf = io.BytesIO()
        save_kwargs = {"format": target_format}
        if target_format == "JPEG":
            save_kwargs["quality"] = 85
        img.save(buf, **save_kwargs)
        data = base64.standard_b64encode(buf.getvalue()).decode("utf-8")
        return data, PIL_FORMAT_TO_MIME[target_format]


def analyze_image(image_path: Path, api_key: str | None = None) -> VisionResult:
    """Send an image to Claude Vision and get structured analysis."""
    key = api_key or ANTHROPIC_API_KEY
    if not key:
        raise ValueError("ANTHROPIC_API_KEY not set")

    image_data, media_type = prepare_image(image_path)

    client = anthropic.Anthropic(api_key=key)
    response = client.messages.create(
        model=VISION_MODEL,
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": VISION_PROMPT,
                },
            ],
        }],
    )

    return parse_vision_response(response.content[0].text)


def parse_vision_response(raw_text: str) -> VisionResult:
    """Parse Claude's JSON response into a VisionResult.

    Tolerates markdown fencing and unescaped quotes in extracted_text by
    extracting individual fields with regex when strict JSON parse fails.
    """
    text = raw_text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = _salvage_fields(text)

    slug = data.get("slug", "untitled") or "untitled"
    slug = slug[:60].strip("-") or "untitled"

    raw_targets = data.get("research_targets", []) or []
    targets = []
    for t in raw_targets:
        if isinstance(t, dict) and t.get("value"):
            targets.append(ResearchTarget(
                type=t.get("type", "unknown"),
                value=str(t["value"]),
                context=t.get("context", "") or "",
            ))

    return VisionResult(
        extracted_text=data.get("extracted_text", ""),
        description=data.get("description", ""),
        tags=data.get("tags", []),
        slug=slug,
        research_targets=targets,
    )


def _salvage_fields(text: str) -> dict:
    """Best-effort field extraction when strict JSON parsing fails."""
    result = {}

    desc_match = re.search(r'"description"\s*:\s*"([^"]*)"', text)
    if desc_match:
        result["description"] = desc_match.group(1)

    slug_match = re.search(r'"slug"\s*:\s*"([^"]*)"', text)
    if slug_match:
        result["slug"] = slug_match.group(1)

    tags_match = re.search(r'"tags"\s*:\s*\[([^\]]*)\]', text)
    if tags_match:
        tags_raw = tags_match.group(1)
        result["tags"] = [t.strip().strip('"') for t in tags_raw.split(",") if t.strip()]

    text_match = re.search(
        r'"extracted_text"\s*:\s*"(.*?)"\s*,\s*"description"',
        text,
        re.DOTALL,
    )
    if text_match:
        result["extracted_text"] = text_match.group(1).replace('\\"', '"').replace("\\n", "\n")

    return result
