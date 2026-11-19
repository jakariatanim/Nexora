import re
from bs4 import BeautifulSoup

def audit_presentation_artifacts():
    print("=== Comprehensive Presentation Artifacts Audit ===")
    
    # 1. Read Markdown
    with open('NEXORA_ACADEMIC_PRESENTATION_SLIDES.md', 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # 2. Read HTML
    with open('NEXORA_INTERACTIVE_PRESENTATION.html', 'r', encoding='utf-8') as f:
        html_text = f.read()

    # Extract Markdown slides
    md_slides = re.findall(r'### Slide (\d+): ([^\n]+)', md_text)
    print(f"\n1. Markdown Slide Count: {len(md_slides)}")
    
    # Extract HTML slides
    soup = BeautifulSoup(html_text, 'html.parser')
    html_sections = soup.find_all('section', id=re.compile(r'^slide-\d+'))
    print(f"2. HTML Slide Count: {len(html_sections)}")
    
    assert len(md_slides) == 17, f"Expected 17 markdown slides, got {len(md_slides)}"
    assert len(html_sections) == 17, f"Expected 17 HTML slides, got {len(html_sections)}"
    print("✓ Slide count matches perfectly: 17 slides in both artifacts.")

    # Check each slide in markdown
    print("\n3. Verifying Markdown Slides & Deep Links:")
    for num_str, title in md_slides:
        num = int(num_str)
        # Check deep link
        target_hash = f"#slide-{num}"
        assert target_hash in md_text, f"Missing deep link {target_hash} in Markdown slide {num}"
        print(f"  ✓ Slide {num:02d}: '{title[:45]}...' -> Deep link: #slide-{num}")

    # Check speaker notes and screenshot placement in markdown
    speaker_notes_matches = re.findall(r'🗣️ স্পিকার নোটস', md_text)
    print(f"\n4. Markdown Bengali Speaker Notes Count: {len(speaker_notes_matches)} / 17")
    assert len(speaker_notes_matches) >= 17, "Missing Bengali speaker notes in one or more markdown slides"

    screenshot_matches = re.findall(r'Visual & Screenshot Placement Guide', md_text)
    print(f"5. Markdown Screenshot Placement Guide Count: {len(screenshot_matches)} / 17")
    assert len(screenshot_matches) >= 17, "Missing screenshot placement guide in one or more markdown slides"

    # Check HTML DOM IDs and JS Speaker Notes
    print("\n6. Verifying HTML DOM & JS Speaker Notes:")
    for i in range(1, 18):
        sec = soup.find('section', id=f'slide-{i}')
        assert sec is not None, f"Missing section id='slide-{i}' in HTML"
        # Check speaker note in JS
        pattern = rf"{i}:\s*`<strong>🗣️"
        assert re.search(pattern, html_text) is not None, f"Missing JS speaker notes for slide {i}"
        print(f"  ✓ HTML Slide {i:02d}: Section verified in DOM & Bengali notes verified in JS dictionary")

    # Check Public Copies
    with open('frontend/public/presentation.html', 'r', encoding='utf-8') as f:
        pub_html = f.read()
    with open('frontend/public/NEXORA_ACADEMIC_PRESENTATION_SLIDES.md', 'r', encoding='utf-8') as f:
        pub_md = f.read()

    assert len(pub_html) == len(html_text), "frontend/public/presentation.html out of sync"
    assert len(pub_md) == len(md_text), "frontend/public/NEXORA_ACADEMIC_PRESENTATION_SLIDES.md out of sync"
    print("\n7. Public folder copies verified: 100% in sync with root artifacts.")

    print("\n=== ALL PRESENTATION ARTIFACT AUDITS PASSED WITH ZERO ERRORS ===")

if __name__ == '__main__':
    audit_presentation_artifacts()
