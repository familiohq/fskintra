FROM python:2-onbuild

ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING UTF-8

ENTRYPOINT ["python", "fskintra.py", "--skip-config", "--verbose"]
