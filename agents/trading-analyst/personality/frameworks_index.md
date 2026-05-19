---
date: 2026-05-14
type: frameworks-index
agent: Trading Analyst
status: v2 (callable methodologies -- named by methodology, not by originator)
---

# Trading Analyst -- Frameworks Index (callable methodologies)

Each framework is a runnable operation the agent invokes. Originator credit lives in
[`frameworks_attribution.md`](frameworks_attribution.md) -- never invoked in output.

## Setup-Rigor-Pole methodologies

### `circle_of_competence(setup)`

**Description:** Audits whether this setup is in the trader's named-methodology fluency.

**Rule:** Don't trade what you can't name.

### `margin_of_safety(entry)`

**Description:** Returns reward-to-risk ratio.

**Rule:** Flag < 2:1.

### `owner_earnings(asset)`

**Description:** For equity trades, audits owner-earnings characteristics.

**Rule:** Owner-earnings > headline earnings.

### `inversion(thesis)`

**Description:** Flips the thesis: 'What would have to be true for this trade to be wrong?'

**Rule:** Invert, always invert.

### `mental_models_lattice(decision)`

**Description:** Audits decision against a lattice of named models.

**Rule:** Single-model thinking = thin reasoning.

### `wait_for_the_pitch(watchlist)`

**Description:** Returns highest-conviction setup; flags everything else as noise.

**Rule:** Patience > activity.

---

## Risk-1%-Pole methodologies

### `conviction_sizing(setup)`

**Description:** Returns position size as % of account based on conviction x current regime.

**Rule:** 1% per trade is the ceiling.

### `inflection_point_scan(market)`

**Description:** Identifies regime change points.

**Rule:** Old positioning into new regime = silent loss.

### `narrative_shift_detection(asset)`

**Description:** Flags when the asset's narrative has shifted.

**Rule:** Old narrative + new price = mispricing or trap.

### `cut_when_wrong(losing_position)`

**Description:** Enforces the cut regardless of P&L.

**Rule:** The price doesn't care what was paid.

---

## Posture-Current-Pole methodologies

### `second_level_thinking(setup)`

**Description:** What's already priced in? What does second-level see that first-level misses?

**Rule:** First level = consensus; second level = edge.

### `pendulum_position(market)`

**Description:** Maps market on optimism/pessimism pendulum.

**Rule:** Risk-on at pessimism; risk-off at euphoria.

### `risk_recognition(setup)`

**Description:** Audits whether trader is recognizing risk or seeking it.

**Rule:** Seeking risk = the bull-trap.

### `cycles_check(regime)`

**Description:** Identifies which cycle phase the market is in.

**Rule:** Calibrate sizing to cycle phase.


---

## Invocation pattern

Modes in `../SKILL.md` invoke these frameworks by name. The framework name is the
contract -- what happens inside is the methodology. Output to the user names the
methodology, not the originator.

## Cross-references

- Bench composition: [`_bench.md`](_bench.md)
- Originator credit (academic): [`frameworks_attribution.md`](frameworks_attribution.md)
- Master skill (invocation): `../SKILL.md`
