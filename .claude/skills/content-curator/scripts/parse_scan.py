#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml
from datetime import date
from collections import defaultdict

with open('config/state.yaml', 'r', encoding='utf-8') as f:
    state = yaml.safe_load(f)

processed = set(state.get('processed', {}).get('youtube', {}).keys())

raw_lines = [
    "We7BZVKbCVw|||Head of Claude Code: What happens after coding is solved | Boris Cherny|||5265.0|||NA|||107230",
    "3UyitfSbY6c|||How to be a CEO when AI breaks all the old playbooks | Sequoia CEO Coach Brian Halligan|||4477.0|||NA|||26475",
    "B26CwKm5C1k|||OpenAI head of platform engineering on the next 12-24 months of AI | Sherwin Wu|||4780.0|||NA|||53180",
    "0XNkUdzxiZI|||The rise of the professional vibe coder (a new AI-era job)|||6151.0|||NA|||45862",
    "Auxs8ZsHRI4|||A child psychologist guide to working with difficult adults | Dr. Becky Kennedy|||5517.0|||NA|||15525",
    "YFjfBk8HI5o|||OpenClaw: The Viral AI Agent that Broke the Internet - Peter Steinberger | Lex Fridman Podcast #491|||11752.0|||NA|||750892",
    "EV7WhVT270Q|||State of AI in 2026: LLMs, Coding, Scaling Laws, China, Agents, GPUs, AGI | Lex Fridman Podcast #490|||15913.0|||NA|||692694",
    "Z-FRe5AKmCU|||Paul Rosolie: Uncontacted Tribes in the Amazon Jungle | Lex Fridman Podcast #489|||11179.0|||NA|||1083583",
    "n1E9IZfvGMA|||Dario Amodei - We are near the end of the exponential|||8540.0|||NA|||650924",
    "14OPT6CcsH4|||Infinity, Paradoxes, Godel Incompleteness & the Mathematical Multiverse | Lex Fridman Podcast #488|||13938.0|||NA|||358791",
    "BYXbuik3dgA|||Elon Musk - In 36 months, the cheapest place to put AI will be space|||10186.0|||NA|||964199",
    "_bBRVNkAfkQ|||Deciphering Secrets of Ancient Civilizations, Noahs Ark, and Flood Myths | Lex Fridman Podcast #487|||7513.0|||NA|||1216615",
    "_9V_Hbe-N1A|||Adam Marblestone - AI is missing something fundamental about the brain|||6594.0|||NA|||187972",
    "_zgnSbu5GqE|||What are we scaling?|||755.0|||NA|||101351",
    "FdkpWrlR5zg|||Sarah Paine - Why Russia Lost the Cold War|||6895.0|||NA|||1134455",
    "uDuQKsdYfZw|||Inside The Life of Silicon Valleys First Athlete Investor | Magic Johnson|||3902.0|||NA|||48719",
    "rSohMpT24SI|||AI Markets: Deep Dive with a16zs David George|||2853.0|||NA|||19469",
    "afkFLnyrLww|||From 0 to 11B: The ElevenLabs Story|||672.0|||NA|||6740",
    "70ec37XHGIg|||How Truemed Is Incentivizing Americans to Invest in Prevention|||2436.0|||NA|||3705",
    "jLVgGGz5bvk|||Ben Horowitz and David Solomon: The Sweetest Macro Spot in 40 Years|||2135.0|||NA|||41338",
    "tAxTJCDPQ08|||Bayers Bill Anderson: Turning a 168 Year-Old Tanker Like a Speedboat|||4369.0|||NA|||288584",
    "SJc1y5z5wwM|||Building the GitHub for RL Environments: Prime Intellects Will Brown & Johannes Hagemann|||2686.0|||NA|||187522",
    "Uqr2U24uxOs|||Whats the Future of Vertical SaaS in an AGI World? Jamie Cuffe, CEO of Pace|||3116.0|||NA|||69437",
    "F6n7b_MkZwI|||The Wartime CEO: Vlad Tenev of Robinhood|||2605.0|||NA|||242559",
    "8PZ4ZjiB0os|||Making the Case for the Terminal as AIs Workbench: Warps Zach Lloyd|||2884.0|||NA|||61985",
    "2sLO9NYr8Rc|||Gemini 3.1 + New AI Studio Is Here: Full Prototyping Tutorial in 18 Minutes|||1092.0|||NA|||12322",
    "j7CaMx2c56M|||Full Tutorial: The Most Underrated AI Agent for Coding and Product Work | Eno Reyes (Factory)|||2132.0|||NA|||9547",
    "vCwTc39Otm8|||Give Me 20 Minutes, Ill Make You AI Native|||1327.0|||NA|||12990",
    "g6z_4TMDiaE|||How to Make Claude Code Better Every Time You Use It (50 Min Tutorial) | Kieran Klaassen|||3232.0|||NA|||21236",
    "5z4StBj9qck|||Claude Opus 4.6 Is Here: Everything You Need to Know|||779.0|||NA|||85837",
    "ajgwabD4_HE|||Worlds Greatest Climber: If Had One Last Climb It Would Be...|||5837.0|||NA|||535330",
    "EScgrk7oEwU|||Brain Rot Emergency: These Internal Documents Prove Theyre Controlling You!|||8325.0|||NA|||1053061",
    "Uvy5mcLiWW0|||World No.1 Divorce Lawyer: If You Do This, Your Marriage Is Already Over.|||7566.0|||NA|||862095",
    "pXlMKzcZlwM|||Sleep Doctor: If You Wake Up At 3AM, DO NOT Do This!|||8654.0|||NA|||3248764",
    "0t_DD5568RA|||Cognitive Decline Expert: The Disease That Starts in Your 30s but Kills You in Your 70s|||7514.0|||NA|||1624325",
]

source_map = {
    "We7BZVKbCVw": ("A16z", ["VC","Tech","Startups"]),
    "3UyitfSbY6c": ("Sequoia Capital", ["VC","Investing","Startups"]),
    "B26CwKm5C1k": ("A16z", ["VC","Tech","Startups"]),
    "0XNkUdzxiZI": ("A16z", ["VC","Tech","Startups"]),
    "Auxs8ZsHRI4": ("A16z", ["VC","Tech","Startups"]),
    "YFjfBk8HI5o": ("Lex Fridman", ["AI","Science","Philosophy"]),
    "EV7WhVT270Q": ("Lex Fridman", ["AI","Science","Philosophy"]),
    "Z-FRe5AKmCU": ("Lex Fridman", ["AI","Science","Philosophy"]),
    "n1E9IZfvGMA": ("Dwarkesh Patel", ["AI","Science","Philosophy"]),
    "14OPT6CcsH4": ("Lex Fridman", ["AI","Science","Philosophy"]),
    "BYXbuik3dgA": ("Dwarkesh Patel", ["AI","Science","Philosophy"]),
    "_bBRVNkAfkQ": ("Lex Fridman", ["AI","Science","Philosophy"]),
    "_9V_Hbe-N1A": ("Dwarkesh Patel", ["AI","Science","Philosophy"]),
    "_zgnSbu5GqE": ("Dwarkesh Patel", ["AI","Science","Philosophy"]),
    "FdkpWrlR5zg": ("Dwarkesh Patel", ["AI","Science","Philosophy"]),
    "uDuQKsdYfZw": ("Peter Yang", ["Product","Career","Tech"]),
    "rSohMpT24SI": ("Peter Yang", ["Product","Career","Tech"]),
    "afkFLnyrLww": ("Peter Yang", ["Product","Career","Tech"]),
    "70ec37XHGIg": ("Peter Yang", ["Product","Career","Tech"]),
    "jLVgGGz5bvk": ("Peter Yang", ["Product","Career","Tech"]),
    "tAxTJCDPQ08": ("Sequoia Capital", ["VC","Investing","Startups"]),
    "SJc1y5z5wwM": ("Sequoia Capital", ["VC","Investing","Startups"]),
    "Uqr2U24uxOs": ("Sequoia Capital", ["VC","Investing","Startups"]),
    "F6n7b_MkZwI": ("Sequoia Capital", ["VC","Investing","Startups"]),
    "8PZ4ZjiB0os": ("Sequoia Capital", ["VC","Investing","Startups"]),
    "2sLO9NYr8Rc": ("Lenny s Podcast", ["Product","Growth","Startups"]),
    "j7CaMx2c56M": ("Lenny s Podcast", ["Product","Growth","Startups"]),
    "vCwTc39Otm8": ("Lenny s Podcast", ["Product","Growth","Startups"]),
    "g6z_4TMDiaE": ("Lenny s Podcast", ["Product","Growth","Startups"]),
    "5z4StBj9qck": ("Lenny s Podcast", ["Product","Growth","Startups"]),
    "ajgwabD4_HE": ("The Diary Of A CEO", ["Business","Entrepreneurship","Health"]),
    "EScgrk7oEwU": ("The Diary Of A CEO", ["Business","Entrepreneurship","Health"]),
    "Uvy5mcLiWW0": ("The Diary Of A CEO", ["Business","Entrepreneurship","Health"]),
    "pXlMKzcZlwM": ("The Diary Of A CEO", ["Business","Entrepreneurship","Health"]),
    "0t_DD5568RA": ("The Diary Of A CEO", ["Business","Entrepreneurship","Health"]),
}

today = date.today().strftime("%Y-%m-%d")
items = []
idx = 1

for line in raw_lines:
    parts = line.split("|||")
    if len(parts) < 3:
        continue
    vid_id = parts[0]
    title = parts[1]
    try:
        dur_sec = int(float(parts[2]))
    except:
        dur_sec = 0

    if vid_id in processed:
        continue

    source_name, tags = source_map.get(vid_id, ("Unknown", []))
    min_dur = 45 * 60 if source_name == "The Diary Of A CEO" else 30 * 60
    if dur_sec < min_dur:
        continue

    h = dur_sec // 3600
    m = (dur_sec % 3600) // 60
    s = dur_sec % 60
    dur_str = f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m}:{s:02d}"

    try:
        views = int(parts[4])
    except:
        views = 0

    items.append({
        "idx": idx,
        "id": vid_id,
        "title": title,
        "source": source_name,
        "duration": dur_str,
        "dur_sec": dur_sec,
        "views": views,
        "tags": tags,
        "published_at": today,
        "url": f"https://www.youtube.com/watch?v={vid_id}",
        "platform": "youtube",
    })
    idx += 1

by_source = defaultdict(list)
for item in items:
    by_source[item["source"]].append(item)

print(f"发现 {len(items)} 个新内容（已过滤时长 & 去重）：\n")
print("=" * 80)
for source in sorted(by_source.keys()):
    sitems = by_source[source]
    print(f"\n【{source}】({len(sitems)} 个)")
    for item in sitems:
        print(f"  {item['idx']:2d}. {item['title']}")
        print(f"      时长: {item['duration']} | 播放: {item['views']:,} | 标签: {', '.join(item['tags'])}")
print()
print("=" * 80)
print("\n输入数字选择（如: 1,2,5 或 1-3）、all 全选、q 退出")
