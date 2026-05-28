# 🧠 OpsMind: AI-Powered Cloud Cost & Security Guardrail

![DevOps](https://img.shields.io/badge/DevOps-Infrastructure__as__Code-blueviolet)
![AI](https://img.shields.io/badge/AI-LLM__Analysis-green)
![Status](https://img.shields.io/badge/Build-Passing-brightgreen)

OpsMind is an automated cloud governance platform designed to intercept high-risk infrastructure changes before they reach production. By integrating LLMs directly into the CI/CD pipeline, OpsMind scans incoming Cloud Architecture blueprints (Terraform) to detect architectural anti-patterns, catastrophic security vulnerabilities, and hidden cloud cost spikes.

---

## 🏗️ System Architecture

When an engineer proposes a cloud infrastructure change, OpsMind automatically intercepts, analyzes, and reports risks:

```text
[ Developer submits Infrastructure Code ]
                  │
                  ▼
      [ GitHub Actions Pipeline ]
                  │ (Triggers Review Event)
                  ▼
         [ OpsMind Backend ] 🧩 ◄───► [ Cloud AI Engine (LLM) ]
                  │                      (Runs Cost & Risk Heuristics)
                  ▼
[ Automated Architectural Report Posted Back to Code Review ]