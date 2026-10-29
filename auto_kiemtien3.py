name: Auto Nhiem Vu (Acc 3)

on:
  workflow_dispatch:
  schedule:
    - cron: '0 */5 * * *'

jobs:
  run-tasks:
    runs-on: ubuntu-latest
    timeout-minutes: 350

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests telethon colorama

      - name: Chay Bot Nhiem Vu Acc 3
        env:
          PYTHONUNBUFFERED: "1"
          PYTHONIOENCODING: "utf-8"
          TELEGRAM_SESSION_B64_ACC3: ${{ secrets.TELEGRAM_SESSION_B64_ACC3 }}
        run: |
          python auto_kiemtien2.py
