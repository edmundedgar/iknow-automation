# iKnow Automation Script

Automates adding Chinese vocabulary items to iKnow.jp.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your credentials:
```
IKNOW_USERNAME=your_email@example.com
IKNOW_PASSWORD=your_password
IKNOW_COURSE_ID=your_course_id
```

## Usage

Run the script:
```bash
python iknow_automation.py
```

The script will:
1. Log in to iKnow.jp
2. Navigate to your course
3. Add vocabulary items defined in the script

## Customization

To add your own vocabulary items, edit the `vocabulary_items` list in `main()`:
```python
vocabulary_items = [
    ("你好", "nǐ hǎo", "hello"),
    # Add more items here
]
```
