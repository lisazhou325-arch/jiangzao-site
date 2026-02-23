#!/usr/bin/env python3
import anthropic

client = anthropic.Anthropic(timeout=600.0)

with open('config/rewrite-prompt.md', 'r', encoding='utf-8') as f:
    prompt_template = f.read()

videos = [
    ('EV7WhVT270Q', 'lexfridman'),
    ('BYXbuik3dgA', 'dwarkesh'),
]

for vid_id, source in videos:
    out_dir = f'content-archive/2026-02-21/youtube_{source}_{vid_id}'
    print(f'Rewriting {vid_id}...', flush=True)

    with open(f'{out_dir}/transcript.md', 'r', encoding='utf-8') as f:
        transcript = f.read()

    if len(transcript) > 12000:
        transcript = transcript[:12000] + '\n\n[内容已截断，以上为前半部分]'

    msg = client.messages.create(
        model='claude-opus-4-6',
        max_tokens=4096,
        messages=[{'role': 'user', 'content': prompt_template + '\n\n' + transcript}]
    )
    rewritten = msg.content[0].text
    with open(f'{out_dir}/rewritten.md', 'w', encoding='utf-8') as f:
        f.write(rewritten)
    print(f'  OK: {len(rewritten)} chars', flush=True)

print('Done')
