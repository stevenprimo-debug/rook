---
title: "7 Skills Quantitative Trading Firms Look For"
source: "https://tradercat.medium.com/7-skills-quant-trading-firms-look-for-96eaa108e4bf"
author:
  - "[[TraderCat]]"
published: 2020-01-06
created: 2026-05-15
description: "And how to pass the toughest interviews in the industry"
tags:
  - "clippings"
---
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*PGJLhywb90CWdFoEgvZELQ.jpeg)

## And how to pass the toughest interviews in the industry

Quantitative trading is the new hot field for STEM majors. With a typical competitive starting compensation around the $250,000 mark and offers of $400,000+ not uncommon (that’s about twice Silicon valley levels), getting hired at one of these competitive firms is perhaps the most lucrative way to start out a career after college. This comes with about half the work hours of a typical investment banking analyst and a pretty sweet performance-based upside in compensation trajectory. Sounds like a pretty good deal, right?

If you haven’t been in the loop, you’re probably wondering (1) why this job exists— after all, there’s no free lunch — and (2) how to get hired. The short answer is that (1) certain skills are required and (2) you need to have those skills. In this article, I’ll break down the seven skills that quantitative trading firms look for when recruiting new talent, based on my experiences from countless interviews as both the interviewer and interviewee.

### Estimating with Confidence

My go-to starter for the technical portion of an interview is a simple Fermi question, a.k.a. a rough estimation of some unknown quantity based on whatever knowledge and reasoning one can muster. One of my favorites is the following:

> **Question:** How many commercial aircraft are flying above the United States at this moment?
> 
> **Answer:** Roughly 5000.

There are a lot of ways to get to a good estimate. For instance, one can estimate how much the average person flies, the size of the average plane, and the population of the United States. Putting these pieces together generally yields a reasonable guess. A typical follow-up might be:

> **Question:** Can you make a 95% percent confidence interval?
> 
> **Question:** I’ll tell you that the actual number is higher than your upper bound. Can you give me a new 95% percent confidence interval?

While most candidates answer the first estimation well, they tend to struggle with the follow-ups. Oftentimes, the process goes something like this:

> **A1:** \[nice reasoning\] maybe 3000. **A2:** 2000–4000. **A3:** 3000–8000.

Take a minute to think why the two confidence intervals are both quite lousy. The first one is too narrow: a 95% confidence interval is equivalent to being willing to bet 19:1 odds that you’re right, so unless you’ve worked in air traffic control, 400–20000 would have been more appropriate. The second one isn’t adjusted enough: the lower bound should be at least 4000 and the higher bound should be far higher (if your 95% confidence interval missed, then there’s a good chance you’ve completely missed the mark).

This process of estimating with confidence might seem pedantic, but quantitative trading is remarkably similar, albeit with more complexity and precision. A rough fair value needs to be established, along with constantly-updated bounds at which you’re willing to buy from and sell to (bet against) others.

### Executing under Pressure

The ability to operate under pressure is almost synonymous with Wall Street. In quantitative trading, this comes in two main forms. The first is mental math, and many candidates are painstakingly slow. In an interview, this could be anything from a simple computation:

> **Question:** Is 14/33 or 31/73 larger?
> 
> **Answer:** 31/73.

To a simple combinatorics problem:

> **Question:** You roll two fair dice; what is the expected value of the difference between the two numbers that are rolled?
> 
> **Answer:** 35/18.

Aim to do these within 15 seconds and 1 minute, respectively. The second is decision-making ability. In an interview, this is often tested using a time-sensitive market:

> **Question:** I draw four cards at random from a standard 52-card deck and flip two of them over; they are both hearts. I am willing to buy and sell the number of distinct suits among the four cards for 2.1 and 2.2, respectively. You have 15 seconds to make a trade (if you would like).
> 
> **Answer:** Roughly 2.37.

Here, it’s unreasonable to compute the exact fraction, but with some analysis, it is not too difficult to see that the value is quite a bit higher than the offer.

Trading requires smart speed, and even though most of the computations are automated, there will be many times when news comes out in the market or a broker sends over a large order that require not only the ability to get a handle on whatever you’re trading is now worth, but to do so quickly and precisely. All this has to be done while factoring in any relevant effects from trades earlier in the day and in different securities.

### Good Old Probability

Probability is perhaps the most fundamental aspect of quantitative trading. While traditional banks have information from fundamental analysis and relationships from business connections, quants have the mathematical rigor from an understanding of probability. As you may have noticed, the previous couple questions already involve a good amount of probability.

## Get TraderCat’s stories in your inbox

Join Medium for free to get updates from this writer.

Interview questions designed to test an understanding of probability are generally more subtle:

> **Question:** Cindy is playing a game of set (try it out [here](https://www.nytimes.com/puzzles/set)). She picks a set out at random (uniform over of all possible sets in the deck). What is the probability that her set contains three different colors?
> 
> **Answer:** 27/40.
> 
> **Question:** Cindy picks ten points uniformly at random in a circular disk. What is the probability that no triangle formed by three of the points contains the center of the disk?
> 
> **Answer:** 5/256.

These two problems, while difficult at a first glance, have short and elegant solutions after a bit of insight. The first is a play on conditional probability: we can choose each attribute of the set to be either all the same (1/3) or all different (2/3); however, they can’t all be the same (1/81), so we exclude that case. The second is a tricky one to break down: we only care about the ray defined by each point; given any ray, we know the probability that the other nine will lie within 180 degrees clockwise of the given ray (1/512); there are 10 rays and each of these events is disjoint, so we add them up.

These two problems also exemplify two of the primary challenges in probability. The first is that it’s hard to tell what you can and cannot do: why is choosing attributes and subtracting a case is equivalent to a random set? The second is that it’s hard to find a clean way to break down the problem: why was the problem broken down into a case on rays and angles per point? Learning how to do so requires a substantial mix of mathematical understanding and effective practice.

### An Interest in the Markets

Yes, in order to trade in the markets, you should be interested in the markets. For one, if you want to trade, you can’t hate your job: you have to be OK with the fact that you’ll be selling out in finance, the fact that almost all the women are in HR, the fact that you don’t leave your desk between 9:30 and 4:00. But more importantly, you need to convince the interviewers that the trading game is one that you’ll be vigorously drawn to. Whether it’s a niche fascination with some market microstructure or a thrill in playing high-level poker (trading is basically professional gambling), potential employers look for signs that a candidate will really dig in and make some dough. In particular, it’s less about being interested in finance and more about the game of finance.

Much of this is addressed in the background portion of the interview — expect your typical “what brought you into trading” or “I see you’re run an investing club…” prompts. In the technical portion, you might be asked to play some variant of a gambling game, such as:

> **Activity:** Each person is dealt a card from a 52-card deck, and is allowed to see their card. Going clockwise, each person bids for the difference between the largest and smallest cards (K=13, Q=12, J=11), and must either increase the bid or sell to the previous bid on their turn.

Not only should you develop a solid strategy over a couple iterations, but you should also have fun playing the game. Indeed, traders can often be found making up trading games to bet on after the close.

Lastly, if you’ve done a finance internship before, be prepared to answer questions related to what you’ve done. For instance, if you were an options trading intern, you might get:

> **Question:** State an options position that is short gamma and long vega.
> 
> **Answer:** Calendar spread (among others).

While being familiar with financial instruments is generally not critical, being able to learn and retain knowledge about them is.

### Modeling and Analysis

The stock market generally operates as a martingale, and finding enough alphas to trade profitably on is difficult due to intense competition. In order to do so, thorough analysis and robust models are required — not just to make money, but to avoid losing money. In pricing a security, there are a myriad possible factors to consider, some of which are significant. For instance, if a biotech company’s new drug is approved, not only will the price of the stock jump due to the profitability of the drug, but a biotech ETF may begin including the company due to the increase in market cap, resulting in a sizable (but benign) buying pressure in the stock. Correctly identifying and incorporating these small details will make or break a trading strategy.

In an interview, you might be taken through the process of developing a model:

> **Question:** Develop a model to estimate the number of cars stuck in traffic in Manhattan at any time up to 48 hours in the future. How would you collect the relevant data and train the model?

You want to be comprehensive yet concise in identifying possible factors, such as time of day, day of week, holidays, events, weather, road construction, accidents, etc., and provide sufficiently intelligent comments on practical ways to gather some data and produce a model.

Analytical skills will also be examined in other portions of the interview. For instance, when playing the gambling game in the previous section, you will be expected to notice any errors in your strategy and respond accordingly. It is extremely important in trading to quickly notice any missing factors or incorrect parameters, so interviewers will be on the lookout for your ability to do so.

### Statistics and Linear Algebra

If (applied) math isn’t your thing, then you might want to familiarize yourself with some of the fundamentals. After all, the modifier quantitative isn’t for naught. While you won’t need to know what an automorphic L-function or a perverse sheaf is, you will need to be comfortable with statistics and linear algebra. Expect questions that test your ability to apply the fundamental concepts rather than your ability to recall esoteric formulas. A question on statistics might look like:

> **Question:** Consider three random variables X, Y, Z for which the correlation between X and Y is 0.6 and between Y and Z is 0.8. Is it possible for X and Z to be independent? What is the maximum possible correlation between X and Z?
> 
> **Answer:** Yes, 0.96.

Simply knowing the definition of correlation isn’t enough to solve the problem. For the first part, we can set X and Z to be independent with variance 1 and Y to be 0.6\*X + 0.8\*Z (also with variance 1). For the second part, the covariance matrix of \[X, Y, Z\] is positive-semidefinite, and the same holds for the correlation matrix; since the determinant is non-negative, we obtain an inequality; solving for corr(X, Z), we solve the quadratic and find that the maximum value is 0.96. Trading firms want candidates who will be able to use statistical principles to reliably assess trading strategies or to not get lost in the multitude of financial instruments (such as these [options](https://finance.yahoo.com/quote/VXX/options/) on an exchange-traded note of futures on an index calculated from options on an index of equities).

For linear algebra, be ready to factor and differentiate matrices. This is generally limited to more research-oriented roles, but many quantitative trading firms are research-driven and require a mastery of these powerful techniques in order to handle the reams of data and sophisticated models used every day.

### Programming with Data

Most quantitative traders are competent coders, often skilled enough to get a job at Facebook or Google. There is a large amount of data that needs to be processed, analyzed, and displayed, and while there are dedicated developer teams, being able to program is indispensable. The language used depends on the firm: some use C++ to test and implement low-latency strategies, some use Microsoft Excel to quickly visualize data and run regressions, most use Python in some capacity or another.

If your prospective role has any amount of quantitative research involved, anything from a typical entry-level software interview is fair game, though with a skew towards algorithms and data structures. There are thousands of practice questions online for these, so I will defer providing a sample question to a interview preparation platform such as [LeetCode](https://leetcode.com/) — the harder questions are generally pretty simple, but the skill lies in being able to reliably find a solution under pressure and code it up quickly.

More specific programming skills, such as managing large databases, building simple interfaces, training statistical models, and general coding habits, are not generally tested for in an interview, but are definitely qualities that quantitative trading firms look for in candidates.

Depending on the specific firm and role, some of these seven skills will be prioritized over others. Research-oriented firms like Radix will focus on probability, statistics/linear algebra, modeling, and coding. Trading-oriented firms like Susquehanna will focus on estimations, mental math, trading enthusiasm, and probability. Hybrid firms like Citadel/Citadel Securities will find a suitable role based on your strengths and weakness and evaluate based on the relevant skills. And lastly, every firm will be paying attention to how well each candidate will fit into the team environment, so clear communication is key.