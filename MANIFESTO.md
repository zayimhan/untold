# UNTOLD — 1973

_An Artist's Manifesto_

---

## Why this medium?

I chose an interactive web experience because the thing I wanted to make is fundamentally about a transaction — something given from one person to something larger than themselves. A painting cannot do that. A generated image sits still. What I needed was a machine that could _receive_ the unsaid thing, recognize it, and give something back.

The web experience is the closest civilian form we have to a confessional. You sit alone with a text field. Nobody is watching. You type something you would not say out loud. The screen is both audience and void. That asymmetry — the intimacy of input, the anonymity of reception — is the emotional architecture the project required.

Early in the design process I had to decide what happened _after_ you typed the thing. A loading spinner felt wrong — it trivialized the weight of what had just been submitted. So instead the screen goes quiet and a single line rises: _while you still have the chance._ Then below it: _say it._ Then _say it_ fades upward and disappears, and _seal it_ appears in its place. The sequence takes about six seconds. Nobody asked me to make it that way. But the moment I removed it in testing, the experience felt like nothing. That sequence is not decoration. It is the pause between saying something and having to live with having said it.

But the web alone is not enough. What transforms it is the archive.

The archive is a collection of 37 fragments: unsent letters, margin notes, things written and folded and never mailed. They span 1968 to 1995. A Vietnam soldier writing to his father the night before a patrol. A woman composing a letter to a man she never called. A worker writing in a factory break room about a colleague whose name will never appear on any wall. None of them sent what they wrote.

When you submit your unspoken thing, the system searches that archive — not by keyword, but by emotional geometry. It finds the historical moment that resonates with yours. Then it writes the lyric the two of you deserve together.

The medium is not incidental. It is the argument.

---

## What caught me?

Dylan wrote "Knockin' on Heaven's Door" for a dying sheriff in Sam Peckinpah's _Pat Garrett & Billy the Kid_ (1973). The sheriff, played by Slim Pickens, has been shot. He walks to a river. His wife follows. He takes off his badge and holds it up to the sky. He cannot use it anymore.

What caught me was not the dying. It was the badge.

A badge is a tool of authority, identity, and obligation. The sheriff's final act is not to fight, not to speak, not even to pray. It is to offer the badge back. To say: _this thing I carried, I am done carrying it._ The knocking is not asking to be let in. It is asking to be allowed to put something down.

That is what the unsaid carries. Not grief alone — though there is grief. But the weight of the thing that was never handed over. The letter that was never mailed. The words that stayed inside until the door closed permanently.

The counterculture of 1967–1973 was living inside that question at civilizational scale. The Vietnam War created an entire generation of people carrying things they could not name. Boys who wrote letters home that they tore up before mailing. Families who received folded flags instead of the conversation they had been waiting for. The anti-war movement was, at its core, a massive collective attempt to say the thing that the official language of the era forbade.

Dylan understood this without needing to explain it. His 1973 output — the soundtrack to Pat Garrett, the stripped plainspokenness of that period — is the sound of someone who has given up ornament. There is nothing to prove. There is only the thing to say, said plainly, before the door closes.

That is what caught me. Not Dylan as icon. Dylan as the man who learned to speak without decoration.

This is why the lyric generator is instructed to write the way it is. Not metaphors. Not abstractions. No similes — the word "like" is explicitly banned in the prompt. Each line must be ten to fifteen words, a complete thought, grounded in something physical: a place, a specific object, a moment in time. The generator is told that a line like "the light is on" is a caption, not a lyric. The target is something like "the kitchen light was still burning when I got back past midnight." That gap — _still burning_, _when I got back_ — is where the emotional weight lives. That is the gap the sheriff's badge opened. The project is built inside it.

---

## AI as what?

In this project, AI is an archivist.

It is not a collaborator in the romantic sense — it does not have feelings about the work. It is not a tool in the dismissive sense — it is not simply executing commands. It occupies a stranger position: it is the keeper of a collection it did not collect, and it reads what you give it with a kind of structural empathy that has no inner life behind it.

The pipeline has five stages, and I want to describe them honestly, because the architecture is a creative decision as much as a technical one.

First: the guardian. Before the pipeline begins, your text passes through a content filter. If it contains profanity or hate speech in any language — Turkish, English, or otherwise — the system stops and asks you to say it nicer. This is not censorship of difficult emotions. It is a boundary between the vulnerable and the abusive. The system is built to hold grief, anger, regret, and shame. It is not built to hold contempt.

Second: the theme interpreter rewrites your input in the voice of a 1973 archivist — not a summary, but a classification. It decides what kind of unsaid thing you brought. The valence: is this grief, anger, longing, relief? The time: is the door still open, or has it closed? The relational target: a parent, a lover, yourself? This rewriting is the most important step in the pipeline. It is the moment your 2024 emotion is translated into 1973 coordinates.

Third: it searches the archive. Both your newly-written annotation and the archive entries are embedded in the same vector space — a mathematical space where emotional distance is measurable as geometry. This is called HyDE, Hypothetical Document Embeddings. The archive was not embedded as raw text. Each entry was embedded via an archivist annotation that describes its emotional content in exactly the same format as your query. When the two vectors are close, it is not because they use the same words. It is because they describe the same shape of silence.

Fourth: an evaluator scores the match. The closest vector is not always the best emotional match — similarity is not resonance. The evaluator asks: does this 1973 voice point in the same emotional direction as the input? If the score falls below seven out of ten, the system moves to the next candidate. It is looking for the letter that _belongs_ with yours, not the one that merely resembles it.

Finally: the lyric is written. Token by token, streamed to the screen one word at a time. It arrives the way a song arrives — you hear each line before you know what the next one will say. The lyric is not about you, and it is not a quotation from the archive. It is a third thing: a voice shaped by the 1973 emotional weather and the texture of the thing you could not say.

What is AI in this relationship? It is the archivist who has read everything and forgotten nothing. It cannot be moved by what it reads. But it can be _accurate_ about it in a way that I — the author — cannot be for another person's unsaid thing. I do not know what you could not say. The archivist does not know either. But it knows how to find the historical moment that lived inside the same shape of silence.

That is the role: not creation, not tool use, but _witness with structure_.

---

## My door

I never saw myself as the one knocking. I saw myself as the one standing behind the door — waiting to see whether the knock would come, whether anyone would choose to act. That is what I believe matters: not the door itself, but what someone decides to do when they are standing in front of it. Action is the only thing that belongs to us.

There is no single threshold in my life I can point to. What I have instead is an accumulation — things I did not say because the moment passed and saying them became impossible, things I could not say because saying them would have caused damage I was not willing to cause, and things I chose not to say because I already knew they would change nothing. Those are three different silences, and they do not feel the same from the inside. But they share the same result: the door stays closed.

I built this because I kept thinking about everyone who carries the same weight. The archive taught me something I needed to see: the unsaid is not rare. It is not a private failure or a personal weakness. The letters from 1968, 1973, 1995 — they are full of people who had every reason to speak and still could not. That did not make the silence smaller. But it made it less lonely. And somewhere in building the pipeline, in watching the archivist find the right historical echo for a shape of feeling I could barely name, I started to believe that saying things is almost always the more rational choice. Not always possible. Not always safe. But more rational than we tell ourselves in the moment when we decide to stay quiet.

If you are sitting at that interface, I want you to pour it out. Let it land somewhere. And if you believe that saying the thing might still change something — that there is still a person on the other side of your door — download what the archive gives you. Send it to them. I built the lyric for that. I built the whole thing for that.

---

The song was written for a dying man who could no longer use his badge. The project is built for everyone who is carrying something they cannot use anymore — a word unsaid, a feeling unfiled, a letter unmailed. They come to the interface. They write it down. The archive finds the historical echo. The lyric is written. The door appears. It knocks.

What happens next is theirs to decide.

---

## AI Tools & Transparency

In accordance with the course's academic integrity requirements, all AI models and APIs used in this project are listed below.

**Runtime pipeline — models that run on every user request:**

| Model                    | Provider | Role in the project                                                                                      |
| ------------------------ | -------- | -------------------------------------------------------------------------------------------------------- |
| `text-embedding-3-small` | OpenAI   | Converts archive annotations and user queries into vectors for cosine similarity search (HyDE retrieval) |
| `gpt-4o-mini`            | OpenAI   | Content guardian (moderation), theme interpretation, match evaluation                                    |
| `gpt-5.5`                | OpenAI   | Lyric generation — the only model that produces creative output visible to the user                      |

**Development — models used during the building of the project:**

| Model                             | Provider  | Role in the project                                                                      |
| --------------------------------- | --------- | ---------------------------------------------------------------------------------------- |
| Claude Opus (claude-opus-4-7)     | Anthropic | Architectural thinking, pipeline design, system prompt engineering, conceptual decisions |
| Claude Sonnet (claude-sonnet-4-6) | Anthropic | Code implementation — backend (FastAPI, Python) and frontend (Angular 21, TypeScript)    |

**What AI generated vs. what the author directed:**
The archive of 37 historical fragments, the HyDE annotation format, the emotional axes used for evaluation, the system prompt constraining the lyric style, and every aesthetic and structural decision in the interface were made by the author. AI models execute within those constraints. The lyric is generated by `gpt-5.5`; the voice it writes in, the rules it follows, and the historical material it draws from were designed by hand.
