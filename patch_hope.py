from pathlib import Path
text = Path('index.html').read_text(encoding='utf-8', errors='ignore')

old_section = '''        <h3>What Just Happened</h3>
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
        </div>'''

new_section = '''        <h3>In the Midst of Tragedy</h3>

        <p>If your heart is heavy today, these words are for you. You do not have to carry this alone.</p>

        <blockquote style="border-left:4px solid #22c55e; padding:0.75rem 1rem; background:rgba(34,197,94,0.08); font-style:italic; color:#4ade80;">
          <p>"Come to me, all who labor and are heavy laden, and I will give you rest. Take my yoke upon you, and learn from me, for I am gentle and lowly in heart, and you will find rest for your souls." — Matthew 11:28-29</p>
        </blockquote>

        <blockquote style="border-left:4px solid #22c55e; padding:0.75rem 1rem; background:rgba(34,197,94,0.08); font-style:italic; color:#4ade80;">
          <p>"For God so loved the world, that he gave his only Son, that whoever believes in him should not perish but have eternal life." — John 3:16</p>
        </blockquote>

        <blockquote style="border-left:4px solid #22c55e; padding:0.75rem 1rem; background:rgba(34,197,94,0.08); font-style:italic; color:#4ade80;">
          <p>"Be strong, and let your heart take courage, all you who wait for the Lord." — Psalm 31:24</p>
        </blockquote>

        <blockquote style="border-left:4px solid #22c55e; padding:0.75rem 1rem; background:rgba(34,197,94,0.08); font-style:italic; color:#4ade80;">
          <p>"The Lord is near to the brokenhearted and saves the crushed in spirit." — Psalm 34:18</p>
        </blockquote>

        <blockquote style="border-left:4px solid #22c55e; padding:0.75rem 1rem; background:rgba(34,197,94,0.08); font-style:italic; color:#4ade80;">
          <p>"Peace I leave with you; my peace I give to you. Not as the world gives do I give to you. Let not your hearts be troubled, neither let them be afraid." — John 14:27</p>
        </blockquote>

        <p>Christ is the hope of the world. And He can become <strong>your</strong> hope — right now, in this moment, no matter what you have lost or what you fear. He offers forgiveness, peace, and a love that nothing can break. He does not wait for the trumpet to offer peace. He stands at the door and knocks.</p>

        <p>But there is also an event coming that will change everything for everyone at once. It will not matter who you are, where you live, or what you believe. The whole world will feel tragedy simultaneously. Families will be torn apart. Nations will be thrown into confusion. Economies will falter. The familiar order will collapse, and every heart will ask the same question: <strong>What is happening?</strong></p>

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
        </div>'''

if old_section in text:
    text = text.replace(old_section, new_section)
    Path('index.html').write_text(text, encoding='utf-8')
    print('updated Hope page opening')
else:
    print('section not found')
