# vocaloid-song-studio

**中文名：V家叙事歌工房**

一套日语优先的原创虚拟歌声歌曲 Skill。它把故事梗概推进为完整的歌曲设计、自然日语歌词、平假名唱读、中文意译、抓耳 Hook、音乐制作 Agent 提示词、LRC、Folia 一键导入包、封面提示词和社媒发布文案。

## 适合什么任务

- 从一句故事梗概创作日语 V 家剧情歌
- 高速 J-pop、电子摇滚、暗黑电子、魔法少女或世界观叙事歌曲
- 检查日语歌词是否自然、可唱、押韵且没有翻译腔
- 把“故事讲清楚”和“副歌抓耳”同时做好
- 生成可直接投给 Suno、Tunee 或其他音乐 Agent 的完整提示词
- 清理生成平台导出的 LRC
- 制作 Folia 一键文件夹导入包
- 生成封面提示词、小红书或其他社媒发布文案

默认输出日语歌词，并附平假名唱读和中文意译。用户明确要求时也可创作中文或其他语言的虚拟歌声歌曲。

## 安装

将整个 `vocaloid-song-studio` 目录复制到客户端的 Skills 目录，或在支持 `.skill` 安装包的客户端中导入发布文件 `vocaloid-song-studio.skill`。

不同客户端的 Skills 目录和导入入口可能不同，请以对应客户端当前文档为准。

## 示例请求

```text
我想写一首 190 BPM 左右的日语电子歌姬歌曲。女高中生以为自己觉醒成魔法少女，最后才发现幻想世界和病房里的物件一一对应。请从故事设计开始，最后给我完整日语歌词、唱读、中文意译和音乐 Agent 提示词。
```

```text
这份日语歌词故事是成立的，但副歌完全记不住。请保留人物和结局，重新设计四行核心 Hook，检查 mora、句尾元音和最终副歌的语义翻转。
```

```text
这个文件夹里已经有 WAV、Tunee 导出的 LRC 和封面。请清理制作提示，按实际演唱歌词生成同名 LRC 和中文翻译，再整理成 Folia 一键导入目录。
```

## 默认交付文件

- `song-manifest.json`
- `lyrics-design.md`
- `lyrics-ja.md`
- `lyrics-reading-zh.md`
- `music-agent-prompt.md`
- `cover-prompt.md`
- `release-copy.md`

音频生成以后，Skill 还可以准备 LRC 与 Folia 导入目录。

## 内置脚本

```bash
python scripts/validate_song_package.py <song-project>
python scripts/clean_lrc.py input.lrc output.lrc
python scripts/build_folia_package.py --audio song.wav --lyrics song.lrc --cover artwork.png --title "曲名" --output release/曲名
python scripts/verify_skill.py .
```

脚本只使用 Python 标准库，不需要安装第三方依赖。

## 《眨眼之外》样本

`samples/mabataki-no-sotogawa/` 是一个完整文本样本，展示：

- 不可靠第一人称和延迟揭示
- 幻想物件与现实物件的双重意象
- 重复 Hook 与最终副歌语义翻转
- 日语歌词、唱读和中文意译的一致性
- 一次性音乐制作 Agent 提示词
- LRC、Folia 和社媒发布文件

样本用于学习工作流，不是可复刻模板。新作品不得复制它的人物、故事、歌词、旋律设想或意象映射。

## 独立性

这个 Skill 不调用或依赖其他 Skill。所有执行说明、模板和验证脚本都包含在包内。

## 许可与商标

代码、模板和文档按 MIT License 发布，详见 `LICENSE`。样本原创文本按同一许可随包提供。

“VOCALOID”是 Yamaha Corporation 的商标。本项目是独立社区创作工具，与 Yamaha、Crypton Future Media 或任何歌声合成软件厂商没有隶属或背书关系。详见 `NOTICE.md`。
