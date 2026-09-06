# 🎤 vocaloid-song-studio

> **把一句故事梗概，变成一首可以生成、可以校验、可以发布的原创日语 V 家叙事歌。**

**V家叙事歌工房** 是一套日语优先的虚拟歌声（Vocaloid-style）歌曲创作 Skill。从故事设计、自然日语歌词、平假名唱读、中文意译、抓耳 Hook，到音乐制作 Agent 提示词、LRC 清理、Folia 一键导入包、封面提示词和社媒发布文案——一首歌从想法到发布的完整链路，全部装在一个 Skill 里。

```
一句设定 ──► 歌曲设计 ──► 日语歌词 ──► 唱读/意译 ──► 制作提示词 ──► LRC/Folia ──► 发布文案
   "女高中生以为觉醒成魔法少女"                                                                    "路灯、白灯、追光"
```

---

## ✨ 它能做什么

| 你给它 | 它还你 |
| --- | --- |
| 一句故事梗概 | 完整歌曲包：设计文档 + 冻结歌词 + 唱读意译 + 制作提示词 |
| 一段翻译腔歌词 | 自然日语重写：mora 估算、句尾元音、可唱性分析 |
| 记不住的副歌 | 四行核心 Hook：重复策略 + 最终副歌语义翻转 |
| WAV + Tunee LRC + 封面 | 清洁歌词、中文翻译时间轴、Folia 一键导入目录 |
| 一首做好的歌 | 封面生成 Prompt + 社媒发布文案（含 AI 参与说明） |

**擅长的曲风**：V 家叙事歌、高速 J-pop、电子摇滚、暗黑电子、魔法少女曲、世界观叙事曲、反转歌、无反转纯上升曲——高速崩塌和温柔绽放都行。

**默认日语**，附平假名唱读和中文意译；明确要求时也可写中文或其他语言。

---

## 🚀 安装

**方式一**：克隆本仓库，把 `vocaloid-song-studio/` 整个目录复制到你客户端的 Skills 目录。

**方式二**：下载 Release 中的 `vocaloid-song-studio.skill` 安装包，在支持该格式的客户端里导入。

```bash
git clone git@github.com:XN-289/vocaloid-song-studio-skill.git
```

> 不同客户端的 Skills 目录位置与导入入口有差异，以你所用客户端的文档为准。
> 脚本仅使用 Python 标准库（3.10+），无需安装任何第三方依赖。

---

## 💬 试一试：三句真实请求

**从零写一首**

```text
我想写一首 190 BPM 左右的日语电子歌姬歌曲。女高中生以为自己觉醒成魔法少女，
最后才发现幻想世界和病房里的物件一一对应。请从故事设计开始，最后给我完整
日语歌词、唱读、中文意译和音乐 Agent 提示词。
```

**修一段记不住的副歌**

```text
这份日语歌词故事是成立的，但副歌完全记不住。请保留人物和结局，重新设计
四行核心 Hook，检查 mora、句尾元音和最终副歌的语义翻转。
```

**把成品整理成可导入的包**

```text
这个文件夹里已经有 WAV、Tunee 导出的 LRC 和封面。请清理制作提示，按实际
演唱歌词生成同名 LRC 和中文翻译，再整理成 Folia 一键导入目录。
```

---

## 📦 一次完整交付长什么样

```text
我的歌曲/
├─ song-manifest.json      结构真源：段落、行数、Hook、唱读
├─ lyrics-design.md        歌曲设计：命题、情绪路径、意象系统、时间轴
├─ lyrics-ja.md            冻结的正式日语歌词（唯一真源）
├─ lyrics-reading-zh.md    逐行平假名唱读 + 中文意译
├─ music-agent-prompt.md   一次性音乐制作委托（可直接投给 Suno / Tunee）
├─ cover-prompt.md         封面生成提示词
└─ release-copy.md         社媒发布包

生成音频后还能追加 ──►
release/曲名/
├─ 曲名.wav / .lrc / .t.lrc / cover.png / .foliaignore   ← Folia 一键导入
```

所有文件从冻结歌词逐字派生，内置校验脚本防止版本漂移。

---

## 🔧 内置工具脚本

```bash
# 从模板一键创建新歌曲项目
python scripts/create_song_project.py --title-ja "夜の標本" --output 我的歌曲

# 校验整个歌曲包（段落/行数/Hook 复现/三文件逐字一致）
python scripts/validate_song_package.py 我的歌曲

# 清理生成平台导出的 LRC（删编曲提示/空行/End，保留唱词与时间戳）
python scripts/clean_lrc.py Tunee_曲名.lrc 曲名.lrc

# 生成 Folia 一键文件夹导入包（不改动源文件）
python scripts/build_folia_package.py --audio song.wav --lyrics song.lrc \
  --translation song.t.lrc --cover art.png --title "曲名" --output release/曲名

# Skill 包自检 + 脚本冒烟测试
python scripts/verify_skill.py .
python scripts/self_test.py
```

---

## 📖 包内结构

```text
vocaloid-song-studio/
├─ SKILL.md                    入口：阶段判断 + 工作流 + 创作原则
├─ references/                 按需加载的 8 份深度文档
│   ├─ workflow.md               完整流程与"唯一真源"管理
│   ├─ story-and-song-design.md  命题、情绪路径、揭示结构、双重意象
│   ├─ japanese-lyrics.md         mora、唱读、翻译腔修复、意译规范
│   ├─ hooks-and-structure.md     三种副歌模式、短视频记忆点设计
│   ├─ production-agent-prompt.md 音乐 Agent 提示词协议
│   ├─ post-production.md         LRC、Folia、封面、社媒发布
│   ├─ originality-and-safety.md  原创边界、声音权利、敏感题材
│   └─ quality-gates.md           逐阶段检查清单与失败回退
├─ assets/templates/           7 个项目模板
├─ scripts/                    6 个标准库工具脚本
└─ samples/mabataki-no-sotogawa/   完整文本样本《眨眼之外》
```

---

## 🌙 样本：《まばたきの外側 / 眨眼之外》

包内附一条**走完全链路的真实文本样本**：

- 不可靠第一人称 + 延迟揭示（Bridge 才让病房声穿透魔法世界）
- 双重意象表：契约手环↔住院腕带、银之杖↔输液架……
- 四行 Hook 三次复现，Final Chorus 最小改字翻转
- 11 段 64 行日语歌词 + 逐行唱读意译 + 制作提示词 + LRC + 发布文案

> 样本用来看「文件之间怎么互相派生」，不是填空模板。新歌不得复用其人物、Hook、意象映射或反转结构——样本 README 里写了明确的禁用清单。

---

## 🛡️ 原创与安全边界

- 只借鉴高层音乐语法，**从零创作**旋律、和声节奏、riff 与歌词
- **不模仿**任何现实歌手、偶像、商业声库的可识别音色，不做声音克隆
- 提示词中不出现艺人名、歌曲名、声库名
- 精神疾病、创伤等题材不做廉价反转与流量猎奇
- 发布文案内置 AI 参与说明，如实描述人机分工

## 📄 许可

- 代码、模板、文档：**MIT License**（见 `LICENSE`）
- 「VOCALOID」是 Yamaha Corporation 的商标。本项目是独立社区工具，与 Yamaha、Crypton Future Media 或任何歌声合成厂商无隶属或背书关系（见 `NOTICE.md`）
