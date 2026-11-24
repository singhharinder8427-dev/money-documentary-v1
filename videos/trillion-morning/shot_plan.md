# "The $1.7 Trillion Morning That Left OpenAI Behind" - SHOT PLAN  [PROPOSAL - no shot code written, nothing rendered]

Script: script.json n001-n055 (~4.4 min). Only LOCKED assets (ASSET_LIBRARY.md). Render: owner's PC (ask again before rendering).
**Owner rules for this video:** ONE continuous film - no hard stops, no wallet chapter; chapter changes use `widgets.chapter_fade`
over the moving picture; the title also lands over the moving Nasdaq tower (no black title card); every set runs its living
background (`ambience.enable()`); subscribe ending instead of the logo outro.
**Ponzi standard + research (`research/APPLY_NEXT_VIDEO.md`):** hook = 4-5 different pictures in the first 10 s (each <= 2.5 s,
first card by ~6 s); a new picture every 2-3 s (long lines split into 2-3 pictures, average ~3.4 s); a beat (card / counter /
stamp / dialogue / place jump) every 20 s at most; whip on place jumps; punch in (1.0 -> 1.25) when stakes turn personal;
counters ease out over ~36 frames and hold >= 20 frames; motifs return changed (the $111.50 ticker, "the list", the walkout).
**Tags:** `widgets.lower_third` in each shot's `hud` at first appearance (and after a long gap): DARIO AMODEI / Co-founder & CEO,
Anthropic - DANIELA AMODEI / Co-founder & President, Anthropic - SAM ALTMAN / CEO, OpenAI - generic roles "THE <ROLE>" / dramatised.
Place tags: `widgets.place_tag` (Nasdaq, Times Square / Nov 19, 2026 - San Francisco, 2021 - ...). Stamps gold.
**Living backgrounds per set** (placements set once per set, see ambience_preview.py / assets_preview.py):
nasdaq_tower = silhouettes + cars + flashes + birds · nasdaq_studio = ticker + gold dust (bell only) + flashes · trading = ticker +
papers · openai_hq = clouds + birds + window lights + silhouettes + cars · megaspeed (2021 office) = silhouettes behind glass +
screens + steam · private_banker = clock + blinds + steam · desk_clean = dust in the lamp beam · newsroom = screens + papers.
**Sounds:** made after the shots are approved (owner) - every movement below gets its sound then.

## HOOK (n001-n009) ~35 s - 13 pictures
| # | Line | Picture | Camera | Animation / beat | Tag / hud |
|---|---|---|---|---|---|
| 1 | n001 "Late Thursday morning, November nineteenth." | night/nasdaq_tower, crowd + cars, ANTHROPIC IS NOW PUBLIC on the LED cylinder | start close on the screen, pull back | camera flashes pop | place tag: NASDAQ, TIMES SQUARE / NOV 19, 2026 |
| 2 | n001 "Wall Street." | night/trading, traders at desks, ticker scrolling | whip in, push | papers flutter | - |
| 3 | n002 "A brand new stock is about to trade..." | close: ticker strip, empty slot "ANT ---" blinking | push 1.0->1.15 | slot blinks gold | - |
| 4 | n003 TRADER "Where's it opening?" | closeup trader (blurred trading floor) | tight | headset, flat mouth, brows up | THE TRADER / dramatised |
| 5 | n004 SECOND TRADER "A hundred and eleven fifty." | closeup trader2, screen behind flips to $111.50 gold | punch 1.0->1.25 | price flip + tick | THE SECOND TRADER / dramatised |
| 6 | n005 (a) "The company is Anthropic." | night/nasdaq_studio, Anthropic mark on the video wall (rough logo), podium | slow push | gold dust | - |
| 7 | n005 (b) "In 2021... people who had just quit OpenAI." | night/megaspeed (2021 office, sign blank), a door swings shut, silhouettes leave behind glass | whip in | door slam | place tag: SAN FRANCISCO / 2021 |
| 8 | n006 (a) "Seven of its founders have already sold shares." | night/desk_clean top-down: 7 share certificates fan out | top-down rotate | paper slides x7 | - |
| 9 | n006 (b) "About $280 million each." | same desk, counter $0->$280,000,000 gold over the certificates | push | counter ticks + ding | - |
| 10 | n007 "Before a single share traded." [CARD] | typed card (first card ~0:16) | static 1.0->1.02 | typewriter | - |
| 11 | n008 (a) "And the company they walked out of?" | night/openai_hq wide, the OpenAI sign, birds | whip in, push to the door | window lights | place tag: OPENAI HQ / SAN FRANCISCO |
| 12 | n008 (b) "Still waiting for its turn." | close on the lit door, one silhouette waiting | push | - | - |
| 13 | n009 "So who really got rich that morning? And who paid for it?" [CARD] | typed card | static | typewriter | - |

## TITLE ~3 s
| 14 | title | night/nasdaq_tower keeps moving; title fades IN over it: THE **$1.7 TRILLION** MORNING (gold on $1.7 TRILLION) | slow pull back | sound logo | - |

## CH1 "The Walkout" (n010-n018) ~40 s - fade chapter card over shot 15
| 15 | n010 "Rewind to 2021." | night/desk_clean, calendar tears back 2026 -> 2021 | top-down | page flips | chapter_fade 1 THE WALKOUT (overlay, first 1.8 s) |
| 16 | n011 (a) "OpenAI is the hottest name in AI." | night/openai_hq (2021), the sign glowing | slow push | window lights | - |
| 17 | n011 (b) "Then a group of its own people walks out." | night/megaspeed: silhouettes walking out past the glass with boxes; door closes | pan with the walkers | footsteps | - |
| 18 | n012 (a) "Among them, siblings Dario and Daniela Amodei." | night/megaspeed (2021 office): dario + daniela walk out past the glass together | tracking | walk cycle | DARIO AMODEI / Co-founder; DANIELA AMODEI / Co-founder |
| 19 | n012 (b) "Their new company is called Anthropic." | closeup dario, Anthropic badge catches light | punch | badge glint | - |
| 20 | n013 ANALYST "They left OpenAI to compete with OpenAI?" | night/office (corner office), analyst at the window | close | brows up | THE ANALYST / dramatised |
| 21 | n014 INVESTOR "Bold." | investor close, sips coffee (steam) | tight | sip | THE INVESTOR / dramatised |
| 22 | n015 ANALYST "Or very expensive." | analyst deadpan, push in | punch 1.0->1.2 | - | - |
| 23 | n016 (a) "Late 2022, OpenAI launches ChatGPT." | night/nasdaq_tower pavement: silhouettes all looking at glowing phones | push | phones light up one by one | place tag: NOV 30, 2022 |
| 24 | n016 (b) "...a hundred million people are using it." | same, counter 0->100,000,000 gold (users) | pull back | counter + ding | - |
| 25 | n017 "Anthropic takes the quieter road... businesses." | night/desk_clean: contracts with company headers slide in, an Anthropic-marked folder signed | top-down | pen signs, paper slides | - |
| 26 | n018 "Remember that choice. It is about to be worth a fortune." | same desk: a gold coin drops on the signed contract | push | coin clink, glint | cliffhanger |

## CH2 "The Swap" (n019-n027) ~50 s - fade chapter card over shot 27
| 27 | n019 (a) "March 2026. OpenAI shuts down Sora," | night/desk_clean: hand holding a phone, Sora app icon (props_ipo.app_icon) | top-down push | - | chapter_fade 2 THE SWAP; date tag MARCH 24, 2026 |
| 28 | n019 (b) "...Six months after launch." | icon greys out, SHUT DOWN gold prop_stamp | punch | stamp thud + shake | - |
| 29 | n020 "A billion-dollar deal with Disney goes with it..." | memo_folder labelled DISNEY DEAL closes; counter $1,000,000,000 -> $0 ORANGE with minus + down arrow | push | folder snap, low tone | - |
| 30 | n021 CLERK "Disney is on the line." | closeup clerk holding phone (phone_in_hand), blurred office | tight | phone buzz | THE CLERK / dramatised |
| 31 | n022 MANAGER "Tell them it was a great six months." | closeup manager rubbing temples | punch | - | THE MANAGER / dramatised |
| 32 | n023 (a) "Then the summer numbers arrive." | night/newsroom, TV wall shows a bar chart | whip in, push to TV | screens flicker | - |
| 33 | n023 (b) "...Anthropic took in $11.6 billion in Q2." | full-frame bar chart (framed stage), Anthropic bar rises, counter $11.6B gold | push | bar grow + ding | label: WSJ, Q2 2026 |
| 34 | n024 (a) "OpenAI? $6.7 billion." | second bar rises shorter, small label COUNTED DIFFERENTLY | static | tick | - |
| 35 | n024 (b) "Still, the headlines called it a first." | night/newsroom desk: newspaper spins in "A FIRST" | top-down | newspaper whoosh | - |
| 36 | n025 "The company that walked out had passed the company it left." [CARD] | typed card | static | typewriter | - |
| 37 | n026 "In September, Sam Altman said OpenAI would not go public in 2026." | night/openai_hq, altman under the sign; then close | push | flash pops | SAM ALTMAN / CEO, OpenAI; date tag SEPT 2026 |
| 38 | n027 "Anthropic wasn't going to wait." | calendar tears to NOVEMBER, gold circle on 19 | punch | page flips | cliffhanger |

## CH3 "Who Gets Paid First" (n028-n038) ~55 s - fade chapter card over shot 39
| 39 | n028 "Here's how an IPO morning really works. In order." | framed stage: a line of 4 icons pops in: BANKS -> BIG INVESTORS -> FOUNDERS -> PUBLIC (public last, small) | static drift | pops | chapter_fade 3 WHO GETS PAID FIRST |
| 40 | n029 (a) "First, the banks set a price." | night/private_banker, banker at desk, night city window | push | clock ticks (ambience) | THE BANKER / dramatised |
| 41 | n029 (b) "Wednesday night, $83 a share. Above the range." | price_tag: $70-78 crossed orange -> $83 slides in | push | tag swing + tick | - |
| 42 | n030 "Then they sell the shares. Mostly to a list of big investors." | investor_list unrolls on the banker's desk | top-down | paper unroll | - |
| 43 | n031 SAVER "Can I buy some at eighty-three?" | saver at the banker's desk, hopeful | close | - | THE SAVER / dramatised |
| 44 | n032 BANKER "Are you on the list?" | banker looks over glasses | punch | - | - |
| 45 | n033 SAVER "What list?" | the list rolls shut in front of her | tight | snap shut | sting |
| 46 | n034 (a) "980 million shares. More than $80 billion." | night/bank_vault: share stacks fill the vault, counter 0->$81B gold | push | stacks thud | - |
| 47 | n034 (b) "The biggest IPO on record." | gold stamp RECORD on the vault door | punch | stamp + shake | - |
| 48 | n035 "Inside that sale, the seven co-founders. Just over 3 million shares each." | desk_clean: 7 certificates, signatures write themselves | top-down | pen scratch x7 | - |
| 49 | n036 BANKER "Seven signatures." | banker closeup stamping | tight | stamp thud | - |
| 50 | n037 CLERK "Seven fortunes." | clerk stacks the signed pages, gold glint | close | paper shuffle | - |
| 51 | n038 "Nearly $2 billion together. All before the public could buy a single share." | night/nasdaq_studio, empty podium, wall clock 9:29 -> bell silent | slow push | clock ticks | cliffhanger |

## TWIST (n039-n042) ~25 s - music cuts, low boom
| 52 | n039 "Then the opening bell rings. And here's what most people miss." | nasdaq_studio, bell (props_ipo.bell) swings, gold dust + flashes | punch 1.0->1.25 | bell ring | - |
| 53 | n040 "Anthropic sold at $83. The stock opened at $111.50." | framed stage: two price tags side by side, the gap between them glows gold | push | tags drop in | - |
| 54 | n041 "That jump didn't go to Anthropic. It went to whoever got shares at $83." [CARD] | typed card | static | typewriter, music silent | - |
| 55 | n042 "By the closing bell, those shares were worth about $14 billion more. In one day." | the investor list glows; counter 0->$14,000,000,000 gold | push | counter + ding | label: our calculation |

## CH4 "The Morning After" (n043-n050) ~45 s - fade chapter card over shot 56
| 56 | n043 "The next day, the stock falls about nine percent. To around $85." | night/trading, ticker turns ANT -9% ORANGE with down arrow; counter 0->9% orange | push | ticker, low tone | chapter_fade 4 THE MORNING AFTER; date tag NOV 20 |
| 57 | n044 "Anyone who bought at the opening price was down almost a quarter." | framed stage: a $111.50 coin loses a quarter slice in orange | static | slice falls | - |
| 58 | n045 TRADER "I bought the open." | trader slumps at desk | close | slump | - |
| 59 | n046 SECOND TRADER "Everybody bought the open." | pan along a row of slumped traders | pan | - | sting |
| 60 | n047 "And one buyer never gets a choice. Index funds." | night/datacenter aisle: fund boxes on a conveyor (props_ipo.fund_box + conveyor) | push | conveyor rumble | - |
| 61 | n048 (a) "Total stock market funds add giants like this within days." | arms pop out of each box and grab an ANT share | tracking | clank x3 | - |
| 62 | n048 (b) "...around eight dollars of every ten thousand." | fund_screen (LOCKED): 10,000 grid, a tiny gold sliver; counter $8 gold | push | ding | label: Morningstar estimate |
| 63 | n049 "But the S&P 500 says no. Not until a full year of trading. And real profits." [CARD] | typed card | static | typewriter | - |
| 64 | n050 "And OpenAI? It reportedly filed in secret in June. It's aiming for 2027." | night/openai_hq, sealed envelope CONFIDENTIAL (anim.envelope + prop_stamp REPORTED), calendar 2027 | push | stamp thud | - |

## ENDING (n051-n055) ~25 s
| 65 | n051 "Back to that Thursday morning. $111.50." | callback: night/nasdaq_tower, same framing as shot 1, ticker shows $111.50 | pull back | flashes | - |
| 66 | n052 "Seven people who once walked out of OpenAI walked away with nearly $2 billion." | 7 silhouettes walk away along the pavement (callback to shot 17) | tracking | footsteps | - |
| 67 | n053 "Their old company is still waiting at the door." | night/openai_hq, the lit door, slow push | push | window light switches on | - |
| 68 | n054 "When OpenAI finally rings its bell, who gets paid first this time?" [CARD] | typed question card, held | static | typewriter | - |
| 69 | n055 "OpenAI's bell is coming... Subscribe, so you're on our list." | night/nasdaq_tower keeps moving; subscribe_button slides up, cursor clicks -> SUBSCRIBED; gold dust | slow push | click + soft chime | video ends here - NO end screen (owner, 24 Nov) |

## Notes for the owner
- 69 pictures for ~4.4 min = one new picture every ~3.8 s on average (hook every ~2.7 s). Typed cards: 6. Counters: 8. Dialogue moments: 5.
- Framed-stage (plain) shots kept to 4 (IPO line-up, bar chart, two price tags, quarter slice) - everything else is a real set.
- Shot 18 uses the 2021 office (night/megaspeed, blank sign) for the walkout; the company there is never named on screen.
- Real people never speak. Altman appears only with his documented September statement (narrated, not quoted).
