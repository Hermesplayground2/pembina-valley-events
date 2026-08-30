from pathlib import Path
text = Path('index.html').read_text(encoding='utf-8', errors='ignore')

old_block = '''<div class="page" id="page-hope">
    <section class="section">
      <div class="card">
        <h2 style="color:#f59e0b;">🕊️ If That Day Comes</h2>
        <p class="muted" style="margin-bottom:12px;">A message of truth, comfort, and direction for the world after the disappearance of millions.</p>
        <div class="spacer"></div>

        <h3>What Just Happened</h3>
        <p>From a biblical perspective, what the world has just witnessed is the fulfillment of ancient prophecy: <strong>the catching up of the church to meet the Lord Jesus Christ in the air.</strong></p>
        <p>This event was spoken of by the apostle Paul in 1 Thessalonians 4:16-17:</p>
        <blockquote style="border-left:4px solid #f59e0b; padding:0.75rem 1rem; background:rgba(245,158,11,0.08); font-style:italic; color:#fbbf24;">
          <p>"The Lord himself will descend from heaven with a cry of command, with the voice of an archangel, and with the sound of the trumpet of God. And the dead in Christ will rise first. Then we who are alive, who are left, will be caught up together with them in the clouds to meet the Lord in the air, and so we will always be with the Lord."</p>
        </blockquote>
        <p>Jesus himself warned that this day would come unexpectedly:</p>
        <blockquote style="border-left:4px solid #f59e0b; padding:0.75rem 1rem; background:rgba(245,158,11,0.08); font-style:italic; color:#fbbf24;">
          <p>"Therefore you also must be ready, for the Son of Man is coming at an hour you do not expect." — Matthew 24:44</p>
        </blockquote>
        <p>The millions who have disappeared are not lost. They have been taken into the presence of God. Their absence from this world is the beginning of their eternal life with Christ.</p>
        <div style="background:rgba(245,158,11,0.1); border-left:4px solid #f59e0b; padding:1rem; border-radius:6px; margin:1rem 0;">
          <p><strong>What has not happened:</strong> The end of the world. The final judgment. The destruction of the earth.</p>
          <p style="margin-top:0.5rem;"><strong>What has happened:</strong> The removal of the church — those who trusted in Jesus Christ as Lord and Savior — to be with Him.</p>
        </div>

        <h3>What to Expect</h3>
        <p><strong>1. Global Confusion and Grief</strong> — Families will mourn. Economies will destabilize. Questions without answers will dominate.</p>
        <p><strong>2. Explanations Will Emerge</strong> — Some will say aliens, some will say government experiment, some will say nothing happened. <strong>The truth is found in the Bible.</strong></p>
        <p><strong>3. A New World Leader Will Rise</strong> — He will bring temporary peace, then demand worship and oppose God.</p>
        <p><strong>4. Persecution of Believers</strong> — Those who come to faith will face severe opposition for a period of seven years.</p>
        <p><strong>5. A System of Control Will Emerge</strong> — Economic systems will require allegiance. Technology will track and control.</p>
        <p><strong>5a. The Mark</strong> — A physical mark will be required to buy or sell. <strong>Do not take this mark under any circumstances.</strong> Revelation warns that those who receive it cannot be saved.</p>
        <p><strong>6. Christ Will Return</strong> — Jesus will come again, defeat evil, and establish His eternal kingdom.</p>

        <h3>How to Prepare</h3>
        <p><strong>1. Read the Bible</strong> — Start with John, then 1 Thessalonians, Matthew 24, Revelation.</p>
        <p><strong>2. Turn to Jesus Christ</strong> — Admit your sin, believe in His death and resurrection, receive Him as Lord.</p>
        <p><strong>3. Find Other Believers</strong> — Look for those reading the Bible, praying, trusting Christ. Form small groups. The church is people, not buildings.</p>
        <p><strong>4. Basic Supplies</strong> — Water, food, medical supplies, cash, flashlight, radio, documents.</p>

        <h3>Finding Peace</h3>
        <p>Fear and grief are natural. But the gospel is this: <strong>God loves you, and He has provided salvation through Jesus Christ.</strong></p>
        <p>If you receive Christ, you will have peace that surpasses understanding, hope for the future, and the promise that He will never leave you.</p>

        <div style="background:#0f172a; border-left:4px solid #22c55e; padding:1rem; border-radius:6px; margin:1rem 0; color:#e2e8f0;">
          <p><strong>A Prayer:</strong> "Lord Jesus, I believe You are the Son of God. I confess that I have sinned and need Your forgiveness. I believe You died on the cross for my sins and rose again. I turn from my sin and receive You as my Lord and Savior. Save me, guide me, and give me peace in this hour of trouble. Amen."</p>
        </div>

        <p style="margin-top:1.5rem;"><strong>To those who have lost loved ones:</strong> They are with Christ. You will see them again if you believe.</p>
        <p><strong>To those who are afraid:</strong> God is still on His throne. He will never leave you.</p>
        <p><strong>To everyone:</strong> Christ is coming again. That is a promise. <strong>Are you ready?</strong></p>
      </div>
    </section>'''

new_block = '''<div class="page" id="page-hope">
    <section class="section">
      <div class="card">
        <h2 style="color:#f59e0b;">🕊️ If That Day Comes</h2>
        <p class="muted" style="margin-bottom:12px;">A message of truth, comfort, and direction for the world after the disappearance of millions.</p>
        <div class="spacer"></div>

        <h3>What Just Happened</h3>
        <p>From a biblical perspective, the world will have witnessed the fulfillment of ancient prophecy: <strong>the catching up of the church to meet the Lord Jesus Christ in the air.</strong></p>
        <p>This event was spoken of by the apostle Paul in 1 Thessalonians 4:16-17:</p>
        <blockquote style="border-left:4px solid #f59e0b; padding:0.75rem 1rem; background:rgba(245,158,11,0.08); font-style:italic; color:#fbbf24;">
          <p>"The Lord himself will descend from heaven with a cry of command, with the voice of an archangel, and with the sound of the trumpet of God. And the dead in Christ will rise first. Then we who are alive, who are left, will be caught up together with them in the clouds to meet the Lord in the air, and so we will always be with the Lord."</p>
        </blockquote>
        <p>Jesus himself warned that this day would come unexpectedly:</p>
        <blockquote style="border-left:4px solid #f59e0b; padding:0.75rem 1rem; background:rgba(245,158,11,0.08); font-style:italic; color:#fbbf24;">
          <p>"Therefore you also must be ready, for the Son of Man is coming at an hour you do not expect." — Matthew 24:44</p>
        </blockquote>
        <p>The millions who will have disappeared are not lost. They will have been taken into the presence of God. Their absence from this world will be the beginning of their eternal life with Christ.</p>
        <div style="background:rgba(245,158,11,0.1); border-left:4px solid #f59e0b; padding:1rem; border-radius:6px; margin:1rem 0;">
          <p><strong>What will not have happened:</strong> The end of the world. The final judgment. The destruction of the earth.</p>
          <p style="margin-top:0.5rem;"><strong>What will have happened:</strong> The removal of the church — those who trusted in Jesus Christ as Lord and Savior — to be with Him.</p>
        </div>

        <h3>What to Expect</h3>
        <p><strong>1. Global Confusion and Grief</strong> — Families will mourn. Economies will destabilize. Questions without answers will dominate.</p>
        <p><strong>2. Explanations Will Emerge</strong> — Some will say aliens, some will say government experiment, some will say nothing happened. <strong>The truth will be found in the Bible.</strong></p>
        <p><strong>3. A New World Leader Will Rise</strong> — He will bring temporary peace, then demand worship and oppose God.</p>
        <p><strong>4. Persecution of Believers</strong> — Those who come to faith will face severe opposition for a period of seven years.</p>
        <p><strong>5. A System of Control Will Emerge</strong> — Economic systems will require allegiance. Technology will track and control.</p>
        <p><strong>5a. The Mark</strong> — A physical mark will be required to buy or sell. <strong>Do not take this mark under any circumstances.</strong> Revelation warns that those who receive it cannot be saved.</p>
        <p><strong>6. Christ Will Return</strong> — Jesus will come again, defeat evil, and establish His eternal kingdom.</p>

        <h3>How to Prepare</h3>
        <p><strong>1. Read the Bible</strong> — Start with John, then 1 Thessalonians, Matthew 24, Revelation.</p>
        <p><strong>2. Turn to Jesus Christ</strong> — Admit your sin, believe in His death and resurrection, receive Him as Lord.</p>
        <p><strong>3. Find Other Believers</strong> — Look for those reading the Bible, praying, trusting Christ. Form small groups. The church is people, not buildings.</p>
        <p><strong>4. Basic Supplies</strong> — Water, food, medical supplies, cash, flashlight, radio, documents.</p>

        <h3>Finding Peace</h3>
        <p>Fear and grief will be natural. But the gospel will be this: <strong>God loves you, and He will have provided salvation through Jesus Christ.</strong></p>
        <p>If you receive Christ, you will have peace that surpasses understanding, hope for the future, and the promise that He will never leave you.</p>

        <div style="background:#0f172a; border-left:4px solid #22c55e; padding:1rem; border-radius:6px; margin:1rem 0; color:#e2e8f0;">
          <p><strong>A Prayer:</strong> "Lord Jesus, I believe You are the Son of God. I confess that I have sinned and need Your forgiveness. I believe You died on the cross for my sins and rose again. I turn from my sin and receive You as my Lord and Savior. Save me, guide me, and give me peace in this hour of trouble. Amen."</p>
        </div>

        <p style="margin-top:1.5rem;"><strong>To those who will have lost loved ones:</strong> They will be with Christ. You will see them again if you believe.</p>
        <p><strong>To those who are afraid:</strong> God will still be on His throne. He will never leave you.</p>
        <p><strong>To everyone:</strong> Christ is coming again. That is a promise. <strong>Are you ready?</strong></p>
      </div>
    </section>'''

if old_block in text:
    text = text.replace(old_block, new_block)
    Path('index.html').write_text(text, encoding='utf-8')
    print('updated Hope page to future tense')
else:
    print('Hope page block not found')
