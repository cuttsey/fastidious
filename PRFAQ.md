# Fastidious: press release and FAQ

## Press release

### Fastidious gives designers one shot at greatness with Claude Code

*Free, open-source design skills that give Claude Code a system of context: they question the brief, decide what the work should mean, start from your own references, check every pixel and present the work, so a single brief becomes a site a designer would put their name to, consistently.*

**London, November 2026.** Fastidious, released today under the MIT licence, is a set of 29 design skills for Claude Code, working alongside 19 more by leading practitioners. It takes one brief from a designer and runs the whole studio around it: framing the problem, deciding what the work should mean, building the brand from that meaning, designing the details people remember, checking the result in a real browser, and presenting it in place, in motion and on film. It asks the designer at every fork, and writes down why every choice was made.

**The problem.** AI has made a first draft almost free, and most first drafts now look the same: a gradient, a headline that would fit any business, three feature cards and a button. Designers know a first impression is the one shot a site gets, and that the difference between good and great lives in purpose, meaning and dozens of small decisions. General-purpose AI tools are built to get to a draft quickly, so they skip exactly the work that makes a site distinctive and defensible. Designers can already build a strong harness around them, with good prompts, skills and tools. What a harness cannot supply on its own is context: what the work is for, what it should mean, whose taste it follows and why each decision was made. Without that, quality depends on the day.

**The solution.** Fastidious is a system of context. It builds that context in the four places where good work becomes great, keeps it in plain files the designer owns, and works from it at every step, so great output is consistent, and it aims to get there from one brief, in one shot.

- **Purpose.** It questions the brief before anyone opens a colour picker, offers alternative frames and lets the designer choose one, then names one person, one pain and one promise a competitor could not repeat.
- **Identity.** It decides what the work should signify, grounded in semiotics, and turns that meaning into a brand system: colour, type, motion and voice.
- **Craft.** It designs the details people remember, such as scroll-driven moments, a cursor and hover gesture from the subject's own world, and signature transitions, and then measures every line of text against the real pixels behind it at every width.
- **Presentation.** It puts the work on devices and in the world, and makes film to show it moving.

Behind its judgement sit 235 production design systems, 97 ranked design sources and 12 exemplar sites taken apart in a real browser. Each designer can add a personal library of the sites and images they admire, and every project starts from that library before anything else.

"The best designers are always dissatisfied," said Jamie Acutt, who built Fastidious. "They know the work could be better, and they keep going until it is. I spent two years teaching Claude to collect taste the way a designer does: to study references closely, take them apart and keep the best parts with the reasons they work. Fastidious is the result. A strong harness gets you a great result on a good day; a system of context is what makes it consistent. It holds your work to the highest standard on purpose, the one you would hold it to on your best day, because a first impression is the one shot the work gets. And it shows its reasoning so you can argue with it."

**How it works.** A designer installs Fastidious in Claude Code with two commands, opens an empty folder and gives it one sentence, such as a site for a small ferry that only runs when the tide allows. Fastidious asks which frame fits, proposes references from the designer's own library, builds the brand and the site, checks it, and leaves its reasoning in plain files the designer keeps: the frame, the positioning, the sign system, the brand system, a numbered decision log and a reason for every detail.

**What we want a designer to say after their first project.** "It asked me better questions than most briefs do, and for once I could see why every choice was made. The site didn't look like AI made it, and where it did, I knew which decision to reopen." *(This is the goal we are designing for, not a quote from a user.)*

**Get started.** Fastidious is free at [github.com/cuttsey/fastidious](https://github.com/cuttsey/fastidious). In Claude Code:

```text
/plugin marketplace add cuttsey/fastidious
/plugin install fastidious@fastidious
```

## Who it is for

- **Designers who are never satisfied with good:** product, brand, web and interaction designers who want a distinctive site, not a plausible one, and who will engage with the questions it asks.
- **Designers moving into Claude Code,** who want their judgement carried into the build instead of being flattened by it.
- **Freelancers and small studios** who pitch and prototype often, and want work they can present and defend, with the reasoning written down.
- **Design leads** who need to show why a direction was chosen, with options, criteria and what was given up recorded as decisions.
- **Developers who care about design** and want a disciplined process instead of a style prompt.

## Who it is not for

- **Anyone who wants a page in one prompt with no involvement.** Fastidious asks you at every fork. If you won't answer, a faster tool will serve you better.
- **Figma-first handoff.** It builds coded sites, mock-ups and film. It does not work inside Figma files.
- **Pixel-exact implementation of an existing design.** It is built to question and design; for a strict build of a finished design, a developer with the file is the right tool.
- **Formal compliance sign-off.** Its accessibility checks, flash screen and contrast measurements are rigorous screening. Regulated or broadcast releases still need a certified audit.
- **Very tight budgets of time or usage.** A full project runs many stages and uses a good part of a Claude allowance. Try it on a real brief when you have time to engage with it.
- **Native mobile apps.** It designs for the web. Some included craft skills cover native motion, but the pipeline builds websites.

## Frequently asked questions

**What exactly do I install?**
Two plugins from one marketplace. `fastidious` holds 29 skills; on first run it offers to install 19 skills by other authors (Impeccable, Taste, Emil Kowalski's skills, GreenSock's GSAP skills and Anatomy) at fixed versions, without ever overwriting a skill you already have. `fastidious-motion` is optional and adds generated stills and film through image and video model APIs.

**What do I need?**
Claude Code, git, Python 3, Node 22 and Chrome. Blender for 3D objects and ffmpeg for film are optional.

**How do I start?**
In an empty folder, run `/fastidious:fastidious` followed by one sentence about the job. To resume, run it again in the same folder and it picks up from `STUDIO-STATE.md`.

**Can I use my own references?**
Yes, and it is designed for that. Keep the sites and images you admire in a personal library (`~/.claude/fastidious/REFERENCES.md`, with images beside it). Every reference carries what to borrow and what to reject. Each project starts from your library before it looks at anything else, and offers to add the best new finds back.

**What do I get back besides the site?**
Plain files you keep: `FRAME.md`, `POSITIONING.md`, `SIGN-SYSTEM.md`, `BRAND-SYSTEM.md`, `REFERENCE-BOARD.md`, `DETAIL-PLAN.md`, a numbered `DESIGN-RATIONALE.md`, a reason for every detail, a verification log and the project's current state.

**Can I use only part of it?**
Yes. Call any specialist directly, for example `/impeccable critique this page` or `/detail-craft plan the signature moments for this site`.

**What does it cost?**
The skills are free under the MIT licence. Running them uses your Claude allowance, and a full project uses a good part of it. `model-switcher` keeps each step on the cheapest model that does it well.

**How do I give feedback?**
Open a project report on GitHub. The question that matters most is: what still looked like AI made it?

## Rude FAQs

The questions people will ask, and the straight answers.

**"Those sites in the film are cherry-picked, or fake."**
They are invented briefs, and the film says so. The sites were built for the film in the way Fastidious works and filmed frame by frame as they really scroll; they are not four unedited Fastidious runs. The real test is your own brief. Run it and post what you get, good or bad.

**"It's more AI slop. Everything will look the same."**
Sameness is the problem Fastidious was built against. Anything a competitor could say unchanged is rejected, references come from your library first, and every effect has to fit the personality the work is meant to have. The four sites in the film share nothing but the method.

**"Nothing good is one shot."**
Agreed, which is why the shot is the brief and not a single prompt. Fastidious asks you at every fork: which frame, which references, which direction. One brief starts it; your decisions shape it.

**"You're automating designers out of a job."**
It does not decide for you. It questions the brief, offers options and records what you chose and what you gave up. It is built to raise the ceiling of what one designer can make, and it is most useful to people with strong judgement.

**"AI has no taste."**
Then lend it yours. Fastidious works from your references, each annotated with what to borrow and what to reject, critiques its own screenshots and writes down the reason for every detail, so you can see where its judgement and yours differ.

**"Scroll-heavy sites are bad for accessibility and performance."**
They can be, so it checks. Reduced motion is designed in, a final accessibility and performance gate has to pass, and every line of text is measured against the pixels actually behind it at phone, tablet and desktop widths. It is screening; a certified audit is still a separate step.

**"Learning from 235 design systems is just copying."**
It studies them for structure: how components are organised and named. It never takes their values without checking the live source, references are cited by name and address, and a reference that turns out to be a direct competitor is dropped.

**"Why not just use v0, Lovable or Framer AI?"**
Use them when speed to a first draft is the goal. Fastidious is for when the reasoning matters: it questions the brief, writes down every decision and checks the result, inside Claude Code and on your own files.

**"It must cost a fortune to run."**
The skills are free. A full project uses a good part of a Claude allowance, which is why it is worth running on real briefs, and why each step runs on the cheapest model that does it well.

**"Does it work with Figma?"**
No. It makes coded sites, mock-ups and film. If your process ends in a Figma file, it is not the right tool yet.

**"Why should I trust a tool built by one person?"**
You don't have to. It is open source under the MIT licence: read every line, every reason it writes down, and the tests that run on every change. Third-party skills are installed from their authors at fixed versions, so nothing changes under you without a deliberate update.
