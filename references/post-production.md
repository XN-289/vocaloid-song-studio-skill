# 后期制作、Folia 与社媒发布

## 目录

1. 成品事实优先
2. LRC 清理
3. 翻译时间轴
4. Folia 一键导入包
5. 封面 Prompt
6. 社媒发布包
7. AI 参与说明
8. 剧透控制

## 1. 成品事实优先

生成完成后，项目可能同时存在：

- 最新正式歌词
- 音乐 Agent 提示词中的锁定歌词
- 平台实际唱出的歌词
- 平台导出的 LRC

LRC 和发布字幕必须对应实际音频。若音频唱的是旧稿，不要用最新草稿覆盖时间轴。先决定是否重生音频；不重生时，以实际唱词为准。

没有音频试听能力时，明确说明只能以平台导出的 LRC 文本作为实际版本证据。

## 2. LRC 清理

生成平台常把制作说明写入 LRC：

```text
[00:01.20](Fast piano and distorted guitars enter)
[02:51.03]最後の言葉 (Whispered)
[03:35.84][End]
```

清洁规则：

- 保留 `ti`、`ar`、`al`、`by`、`offset` 等合法元数据。
- 保留有实际歌词的时间行。
- 删除纯制作说明行。
- 删除空时间行。
- 删除行尾括号制作标签。
- 删除 `[End]`。
- 保持原时间戳和顺序。
- 不自动“纠正”平台实际唱出的字词。

运行：

```bash
python scripts/clean_lrc.py Tunee_title.lrc title.lrc
```

若需保留对白角色标签，使用 `--keep-role-labels`。

## 3. 翻译时间轴

`.t.lrc` 与主 LRC 使用相同时间戳，每条中文翻译对应同一唱句。

要求：

- 不提前剧透。
- 不逐字复制日语词序。
- 不添加主歌词没有的解释。
- 行数和时间戳与主 LRC 一致。
- 对白角色保持一致。

中文原唱通常不需要重复的 `.t.lrc`。

## 4. Folia 一键导入包

### 最小结构

```text
<title>/
├─ <title>.wav
├─ <title>.lrc
├─ <title>.t.lrc
├─ cover.png
├─ .foliaignore
└─ Folia导入说明.md
```

`.t.lrc` 可选。

### 规则

- Folia 按同路径同基础名配对音频与歌词。
- `cover.png`、`cover.jpg`、`cover.jpeg` 是优先文件夹封面名。
- 同一目录中的每个支持音频会成为一个条目。
- 保留 WAV 和 MP3 备份时，用 `.foliaignore` 排除非主音频。
- 原始平台 LRC 和原封面可以保留，但应忽略，避免被识别或造成混乱。

运行：

```bash
python scripts/build_folia_package.py \
  --audio song.wav \
  --lyrics song.lrc \
  --translation song.t.lrc \
  --cover artwork.png \
  --title "歌曲标题" \
  --output release/歌曲标题
```

脚本复制文件，不覆盖源素材。若输出目录已存在且内容冲突，默认停止；显式使用 `--force` 才覆盖脚本自己管理的目标文件。

## 5. 封面 Prompt

封面 Prompt 写清：

- 比例和目标尺寸
- 主体年龄、姿态和画面位置
- 关键物件
- 前景、中景、背景
- 色彩对比
- 镜头、光线与媒介
- 留白位置
- 与歌曲结局相关但不剧透的暗示
- Negative Prompt
- 不生成复杂文字、品牌、水印

对于反转歌，封面只展示表层世界或双重意象，不直接展示真相物件。

### 通用模板

```text
A square original Japanese vocal-synth single cover. [Character and action]. [Key object]. [Surface-world setting]. Subtle visual inconsistency suggesting [hidden layer] without revealing it. [Palette], [lighting], [camera], [medium], clean composition, strong negative space, no text, no logo, no watermark.
```

## 6. 社媒发布包

默认交付：

- 1 个主标题
- 8 至 15 个备选标题
- 长正文
- 短正文
- 封面文案
- 视频前三秒字幕
- 置顶评论
- 5 至 8 个标签
- AI 参与说明
- 剧透控制建议

### 正文顺序

1. 用一个具体动作、时间或物件开场。
2. 讲人物当时理解的故事。
3. 连接听众经验时承认差异，不强行代表所有人。
4. 停在一个疑问、动作或变化后的物件。
5. 最后另起一段说明 AI 参与。

不要以“这是我用 AI 做的一首歌”开场。先让作品吸引人，再说明制作方式。

## 7. AI 参与说明

根据实际情况写清人和 AI 的分工：

```text
故事核心和创作方向来自我的设想。人物细节、日语歌词、作曲、虚拟演唱与视觉呈现使用 AI 辅助完成，我对故事走向和最终结果进行了选择与调整。
```

若人完成了歌词或作曲，不要笼统说全部由 AI 完成。若平台要求 AI 标签，按平台规则使用。

## 8. 剧透控制

- 标题可以露出情绪，不直接念真相。
- 封面不展示最终揭示物件。
- 正文停在音乐即将完成揭示的位置。
- 预览片段优先选第一或第二副歌，不使用结尾全部反转。
- 评论区可在后续笔记发布完整解读。
- 不用疾病、死亡或创伤标签猎奇引流。

发布文案仍需首先是一段好读的故事，不把“反转”当作唯一卖点。
