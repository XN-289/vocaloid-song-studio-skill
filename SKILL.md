---
name: vocaloid-song-studio
description: Creates complete original Japanese-first vocal-synth and Vocaloid-style narrative song projects, from story design and natural Japanese lyrics to memorable hooks, production-agent prompts, pronunciation guides, LRC cleanup, Folia import folders, cover prompts, and social release copy. Use when the user wants to create, rewrite, produce, package, or publish an original V家、Vocaloid、虚拟歌姬、电子歌姬 or vocal-synth song, especially from a story brief, lyric draft, music-agent prompt, generated LRC, or finished-audio folder; also use for Japanese story songs, high-speed J-pop/electro-rock hooks, mora and pronunciation checks, final-chorus reversals, and Suno/Tunee-to-Folia workflows.
license: MIT
compatibility: File read/write tools are required. Python 3.10+ is optional for bundled validation, LRC cleanup, and Folia packaging scripts. Audio generation requires a separate music platform or production agent.
metadata:
  version: "1.0.0"
  display-name: "V家叙事歌工房"
  default-language: "Japanese"
---

# V家叙事歌工房

把一个故事做成可生成、可校验、可发布的原创虚拟歌声歌曲包。默认写自然日语，附平假名唱读和中文意译；用户明确要求时可改用其他语言。

## 独立运行

本 Skill 自包含。不要调用、要求或委托任何其他 Skill。需要的方法、模板与脚本都在当前目录中。

## 先判断用户处于哪一阶段

1. **只有想法**：从故事与歌曲设计开始。
2. **已有设计或歌词**：保留已确认内容，只补缺失环节。
3. **已有音乐 Agent 提示词**：审查原创边界、歌词锁定、生成路径和验收规则。
4. **已有音频或 LRC**：以实际唱词为准做时间轴、封面、Folia 和发布包。
5. **只要其中一项**：只交付该项，不强迫走完整流程。

用户说“不用确认”或“直接一次性输出”时，自行采用合理默认值连续完成。否则只询问会显著改变人物、结局、语言或音乐方向的决定。

## 标准工作流

1. 读取现有文件，列出事实、已冻结内容和缺口。
2. 写一句创作命题和 6 至 8 步情绪路径。
3. 确定人物、叙事视角、揭示时机、双重意象和声音叙事。
4. 先设计歌名、核心 Hook、重复策略与最终副歌变化，再写主歌。
5. 写正式歌词，完成自然语言、可唱性、押韵、Hook 和原创性复核。
6. 冻结歌词，再派生唱读、中文意译和音乐 Agent 提示词，禁止版本漂移。
7. 有成品音频后，核对实际唱词；音频与草稿冲突时，以实际演唱版本制作 LRC。
8. 生成封面提示词、Folia 文件夹和社媒发布文案。
9. 运行确定性验证，并如实区分文本检查与真实试听。

完整阶段说明见 [references/workflow.md](references/workflow.md)。

## 按需读取

- 故事、角色、反转、双重意象： [references/story-and-song-design.md](references/story-and-song-design.md)
- 日语自然度、mora、唱读、翻译： [references/japanese-lyrics.md](references/japanese-lyrics.md)
- 抓耳副歌、重复、押韵、短视频 Hook： [references/hooks-and-structure.md](references/hooks-and-structure.md)
- 一次性音乐制作 Agent 提示词： [references/production-agent-prompt.md](references/production-agent-prompt.md)
- LRC、封面、Folia、社媒发布： [references/post-production.md](references/post-production.md)
- 原创性、声音模仿、敏感题材： [references/originality-and-safety.md](references/originality-and-safety.md)
- 交付前检查与失败回退： [references/quality-gates.md](references/quality-gates.md)

只读当前任务需要的文件，不要一次加载全部参考资料。

## 默认完整交付

```text
<song-project>/
├─ song-manifest.json
├─ lyrics-design.md
├─ lyrics-ja.md
├─ lyrics-reading-zh.md
├─ music-agent-prompt.md
├─ cover-prompt.md
└─ release-copy.md
```

生成音频后可增加：

```text
release/<title>/
├─ <title>.wav
├─ <title>.lrc
├─ <title>.t.lrc
├─ cover.png
├─ .foliaignore
└─ Folia导入说明.md
```

从 [assets/templates](assets/templates) 复制所需模板。用 `scripts/validate_song_package.py` 检查文本包，用 `scripts/clean_lrc.py` 清理生成平台 LRC，用 `scripts/build_folia_package.py` 生成一键导入目录。

## 关键创作原则

- 先让歌作为歌成立，再让故事反转成立。
- Hook 占领记忆靠整段复现和语义变化，不靠连续喊歌名。
- 日语押韵依靠句尾元音、关键词复现和内部音节，不强迫每句同一语法结尾。
- 动作、物件和对白已经表达情绪时，停止解释。
- 只借鉴高层音乐语法，从零创作旋律、和声节奏、riff、歌词和声音动机。
- 不模仿现实歌手、具体声库或创作者的可识别声纹与专属风格。
- 不把疾病、创伤或边缘处境当作廉价反转和流量猎奇。

## 样本使用规则

`samples/mabataki-no-sotogawa/` 展示一条完整链路。先读其中的 `README.md`，再按当前问题选择单个样本文件。学习结构、版本冻结和声音叙事，不复制人物名、剧情、Hook、意象映射或具体措辞。

## 完成声明

只有实际运行过相应检查，才能说结构或文件通过。没有在音乐平台生成和试听时，明确写“文本制作包已完成，音频效果尚未验证”。
