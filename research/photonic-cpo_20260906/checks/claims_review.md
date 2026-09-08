# 主張⇔引用 独立レビュー表

レポートを書いた者以外が記入する。引用文だけを読み、
その引用が主張を支持しているかを判断する（原文に戻ってもよい）。

判定: `支持` / `不支持` / `部分的` / `判断不能`

**不支持・部分的が1件でもあれば、レポートを修正してからGBをやり直す。**

| # | 箇所 | 主張 | 根拠 | 種別 | 引用（原文） | 判定 | コメント |
|---|---|---|---|---|---|---|---|
| 1 | report.md:L13 | - 事実：いまAIデータセンターで実際に製品化が進む光電融合は、**ネットワークの「スイッチ」に光を同梱する形（CPO＝スイッチのASICと同じパッケージに光変 | E-0002 | fact | integrating co-packaged optics (CPO) directly onto the ASIC, overcoming the limits of electrical signaling in large-scal | 支持 | 引用は当該事実を支持 |
| 2 | report.md:L13 | - 事実：いまAIデータセンターで実際に製品化が進む光電融合は、**ネットワークの「スイッチ」に光を同梱する形（CPO＝スイッチのASICと同じパッケージに光変 | E-0020 | fact | With commercial availability for NVIDIA Quantum-X InfiniBand switches set for early 2026 and Spectrum-X Ethernet switche | 支持 | 引用は当該事実を支持 |
| 3 | report.md:L13 | - 事実：いまAIデータセンターで実際に製品化が進む光電融合は、**ネットワークの「スイッチ」に光を同梱する形（CPO＝スイッチのASICと同じパッケージに光変 | E-0021 | fact | With up to 409.6 terabits-per-second (Tb/s) bandwidth, Spectrum-X Ethernet Photonics enables massive generative AI workl | 支持 | 引用は当該事実を支持 |
| 4 | report.md:L14 | レーザーは外部の光源（Lumentumが供給）から「光の入力」としてパッケージへ差し込む構成で、チップ上ではもっぱら光の"点滅"（変調）と受光を行う 。 | E-0013 | fact | with Lumentum providing lasers for the Spectrum-X product and Coherent collaborating on silicon photonics | 支持 | 引用は当該事実を支持 |
| 5 | report.md:L14 | レーザーは外部の光源（Lumentumが供給）から「光の入力」としてパッケージへ差し込む構成で、チップ上ではもっぱら光の"点滅"（変調）と受光を行う 。 | E-0014 | fact | combines 18 silicon photonics engines, enabling 324 optical connections and 288 data links from 36 laser inputs | 支持 | 引用は当該事実を支持 |
| 6 | report.md:L14 | レーザーは外部の光源（Lumentumが供給）から「光の入力」としてパッケージへ差し込む構成で、チップ上ではもっぱら光の"点滅"（変調）と受光を行う 。 | E-0015 | fact | It is the world's first 1.6 Tb/s CPO, based on a technology called a micro ring modulator (MRM). It is completely built | 支持 | 引用は当該事実を支持 |
| 7 | report.md:L15 | - 事実：**GPU同士の最短接続（スケールアップ／NVLink）は現在ケーブル（電気）**で、これを光化するのはNVIDIA自身が「将来のロードマップ」と位置 | E-0030 | fact | NVLink Switch trays and NVLink spine of 5,000 cables form a single all-to-all topology so any GPU can communicate with a | 支持 | 引用は当該事実を支持 |
| 8 | report.md:L15 | - 事実：**GPU同士の最短接続（スケールアップ／NVLink）は現在ケーブル（電気）**で、これを光化するのはNVIDIA自身が「将来のロードマップ」と位置 | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 支持 | 引用は当該事実を支持 |
| 9 | report.md:L16 | 当面（〜2026年）はスイッチ層でのCPO＋外部光源が主流、という順序になる 。 | E-0004 | fact | The first generation is an optical engine for OSFP connectors, offering 1.6 Tb/s data transfer while reducing power cons | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 10 | report.md:L16 | 当面（〜2026年）はスイッチ層でのCPO＋外部光源が主流、という順序になる 。 | E-0013 | fact | with Lumentum providing lasers for the Spectrum-X product and Coherent collaborating on silicon photonics | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 11 | report.md:L16 | 当面（〜2026年）はスイッチ層でのCPO＋外部光源が主流、という順序になる 。 | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 12 | report.md:L18 | ** 理由：一次資料（NVIDIA公式・NTT公式）で骨格は固いが、性能値の多く（電力効率3.5〜5倍など）は**ベンダー自身の主張で独立検証がなく** 、評価 | E-0007 | fact | They integrate optics innovations with 4x fewer lasers to deliver 3.5x more power efficiency, 63x greater signal integri | 支持 | 引用は当該事実を支持 |
| 13 | report.md:L18 | ** 理由：一次資料（NVIDIA公式・NTT公式）で骨格は固いが、性能値の多く（電力効率3.5〜5倍など）は**ベンダー自身の主張で独立検証がなく** 、評価 | E-0008 | fact | NVIDIA CPO technology significantly reduces network power, enabling 5x better power efficiency over pluggable transceive | 支持 | 引用は当該事実を支持 |
| 14 | report.md:L21 | - 現在は発光を外部光源に置きスイッチ層でCPO化する段階だが 、これが覆り、GPU（演算チップ）と同一パッケージに発光レーザーまで内蔵した量産品が近い将来（数 | E-0013 | fact | with Lumentum providing lasers for the Spectrum-X product and Coherent collaborating on silicon photonics | 支持 | 引用は当該事実を支持 |
| 15 | report.md:L21 | - 現在は発光を外部光源に置きスイッチ層でCPO化する段階だが 、これが覆り、GPU（演算チップ）と同一パッケージに発光レーザーまで内蔵した量産品が近い将来（数 | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 支持 | 引用は当該事実を支持 |
| 16 | report.md:L22 | - スケールアップ（GPU間最短）が現在ケーブル接続である状態  が長く続く、または逆に急速に光化すれば、時間軸の描像は変わる。 | E-0030 | fact | NVLink Switch trays and NVLink spine of 5,000 cables form a single all-to-all topology so any GPU can communicate with a | 支持 | 引用は当該事実を支持 |
| 17 | report.md:L35 | 狙いは消費電力の削減  と、より遠く・より大量のデータ伝送 。 | E-0003 | fact | Fiber connects directly with the optical engine that sits beside the ASIC, reducing electrical loss to only ~4 dB and sl | 支持 | 引用は当該事実を支持 |
| 18 | report.md:L35 | 狙いは消費電力の削減  と、より遠く・より大量のデータ伝送 。 | E-0025 | fact | the Tier 1 switch is relocated to the end of the row. This configuration dramatically increases the distance between ser | 支持 | 引用は当該事実を支持 |
| 19 | report.md:L37 | いま製品化の主役である**CPO（Co-Packaged Optics＝同梱光）**とは、これまでスイッチ前面に"挿していた"着脱式の光モジュールを、**スイッ | E-0001 | fact | Replacing pluggable transceivers with silicon photonics on the same package as the ASIC, NVIDIA CPO innovations provide | 支持 | 引用は当該事実を支持 |
| 20 | report.md:L37 | いま製品化の主役である**CPO（Co-Packaged Optics＝同梱光）**とは、これまでスイッチ前面に"挿していた"着脱式の光モジュールを、**スイッ | E-0002 | fact | integrating co-packaged optics (CPO) directly onto the ASIC, overcoming the limits of electrical signaling in large-scal | 支持 | 引用は当該事実を支持 |
| 21 | report.md:L37 | 置き換える対象は、着脱式トランシーバとその長い電気配線 。 | E-0003 | fact | Fiber connects directly with the optical engine that sits beside the ASIC, reducing electrical loss to only ~4 dB and sl | 支持 | 引用は当該事実を支持 |
| 22 | report.md:L39 | この距離では電気配線で信号が保たず、光が必須になる、というのが駆動力である 。 | E-0025 | fact | the Tier 1 switch is relocated to the end of the row. This configuration dramatically increases the distance between ser | 支持 | 引用は当該事実を支持 |
| 23 | report.md:L39 | Huang氏は、従来方式ではGPU1個あたり6個のトランシーバで180W・$6000かかり、100万GPUなら180メガワットに達すると説明している（数値はNV | E-0026 | fact | each of those GPUs would require six individual transceivers, meaning a power consumption of 180 Watts and a cost of $60 | 支持 | 引用は当該事実を支持 |
| 24 | report.md:L43 | 光を電気に代える「境界」が、外側から内側へ段階的に寄っていく ――これが本調査の背骨である。 | E-0004 | fact | The first generation is an optical engine for OSFP connectors, offering 1.6 Tb/s data transfer while reducing power cons | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 25 | report.md:L43 | TSMCの光基盤「COUPE」は3段階で進むとされ、**第1=コネクタ用（着脱式相当、1.6Tb/s）→ 第2=パッケージ同梱CPO（6.4Tb/s、基板レベル | E-0004 | fact | The first generation is an optical engine for OSFP connectors, offering 1.6 Tb/s data transfer while reducing power cons | 支持 | 引用は当該事実を支持 |
| 26 | report.md:L47 | NVIDIAの2026年の製品は、この第2段階（スイッチのパッケージ内CPO）に当たる 。 | E-0002 | fact | integrating co-packaged optics (CPO) directly onto the ASIC, overcoming the limits of electrical signaling in large-scal | 支持 | 引用は当該事実を支持 |
| 27 | report.md:L47 | NVIDIAの2026年の製品は、この第2段階（スイッチのパッケージ内CPO）に当たる 。 | E-0020 | fact | With commercial availability for NVIDIA Quantum-X InfiniBand switches set for early 2026 and Spectrum-X Ethernet switche | 支持 | 引用は当該事実を支持 |
| 28 | report.md:L47 | 第3段階（プロセッサ・パッケージ内）は計画として示されるが時期は確定的でない 。 | E-0004 | fact | The first generation is an optical engine for OSFP connectors, offering 1.6 Tb/s data transfer while reducing power cons | 支持 | 引用は当該事実を支持 |
| 29 | report.md:L47 | そしてGPU同士の最短接続（スケールアップ）は、現状ケーブル接続で、光化は将来ロードマップである 。 | E-0030 | fact | NVLink Switch trays and NVLink spine of 5,000 cables form a single all-to-all topology so any GPU can communicate with a | 支持 | 引用は当該事実を支持 |
| 30 | report.md:L47 | そしてGPU同士の最短接続（スケールアップ）は、現状ケーブル接続で、光化は将来ロードマップである 。 | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 支持 | 引用は当該事実を支持 |
| 31 | report.md:L49 | 推論：したがって「光がチップに近づく」流れは実在するが、2026年時点の到達点はスイッチのパッケージ内までで、演算チップ（GPU）そのものへ光が入り込むのはこれ | E-0004 | fact | The first generation is an optical engine for OSFP connectors, offering 1.6 Tb/s data transfer while reducing power cons | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 32 | report.md:L49 | 推論：したがって「光がチップに近づく」流れは実在するが、2026年時点の到達点はスイッチのパッケージ内までで、演算チップ（GPU）そのものへ光が入り込むのはこれ | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 33 | report.md:L49 | 推論：したがって「光がチップに近づく」流れは実在するが、2026年時点の到達点はスイッチのパッケージ内までで、演算チップ（GPU）そのものへ光が入り込むのはこれ | E-0030 | fact | NVLink Switch trays and NVLink spine of 5,000 cables form a single all-to-all topology so any GPU can communicate with a | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 34 | report.md:L53 | 集めた資料が繰り返し挙げる主戦場は**電力**で、その源泉は**電気配線での信号損失**である 。 | E-0003 | fact | Fiber connects directly with the optical engine that sits beside the ASIC, reducing electrical loss to only ~4 dB and sl | 支持 | 引用は当該事実を支持 |
| 35 | report.md:L53 | 集めた資料が繰り返し挙げる主戦場は**電力**で、その源泉は**電気配線での信号損失**である 。 | E-0005 | fact | This segmented journey incurs substantial electrical loss, up to 22 dB for 200 gigabit-per-second channels | 支持 | 引用は当該事実を支持 |
| 36 | report.md:L57 | 具体的には、着脱式では信号がASICから基板・コネクタを経て遠回りするため200Gb/sチャネルで22dBに達する電気損失が生じ、ポートあたり約30Wを消費する | E-0005 | fact | This segmented journey incurs substantial electrical loss, up to 22 dB for 200 gigabit-per-second channels | 支持 | 引用は当該事実を支持 |
| 37 | report.md:L57 | 具体的には、着脱式では信号がASICから基板・コネクタを経て遠回りするため200Gb/sチャネルで22dBに達する電気損失が生じ、ポートあたり約30Wを消費する | E-0006 | fact | The result is a higher power draw (often 30W per interface) | 支持 | 引用は当該事実を支持 |
| 38 | report.md:L57 | CPOでは光エンジンをASICの隣に置きファイバ直結にすることで、損失は約4dB、電力は9W程度まで抑えられるとされる 。 | E-0003 | fact | Fiber connects directly with the optical engine that sits beside the ASIC, reducing electrical loss to only ~4 dB and sl | 支持 | 引用は当該事実を支持 |
| 39 | report.md:L57 | さらにCPOはDSP（信号を補正する処理チップ）リタイマーを省け、遅延低減にも効くという 。 | E-0009 | fact | NVIDIA CPO doesn't require digital signal processing (DSP) retimers, reducing network latency | 支持 | 引用は当該事実を支持 |
| 40 | report.md:L59 | ただし電力効率の倍率（3.5倍、のち製品ページで5倍）はNVIDIA自身が公表した主張であり、第三者による実測は本周回では未取得である 。 | E-0007 | fact | They integrate optics innovations with 4x fewer lasers to deliver 3.5x more power efficiency, 63x greater signal integri | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 41 | report.md:L59 | ただし電力効率の倍率（3.5倍、のち製品ページで5倍）はNVIDIA自身が公表した主張であり、第三者による実測は本周回では未取得である 。 | E-0008 | fact | NVIDIA CPO technology significantly reduces network power, enabling 5x better power efficiency over pluggable transceive | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 42 | report.md:L59 | スケールアップ網の文脈でNVIDIAは、評価は「時間・電力・設置面積あたりのトークン処理量」で見るべきとし、実効性能・耐障害性・成熟度/サプライチェーンの3点を | E-0011 | fact | Delivered, full-system performance determines how many tokens can be processed and produced per unit time, power, and fa | 支持 | 引用は当該事実を支持 |
| 43 | report.md:L59 | スケールアップ網の文脈でNVIDIAは、評価は「時間・電力・設置面積あたりのトークン処理量」で見るべきとし、実効性能・耐障害性・成熟度/サプライチェーンの3点を | E-0012 | fact | The Key Metrics for Scale-Up Networking in AI Factories | 支持 | 引用は当該事実を支持 |
| 44 | report.md:L61 | 注意（トレードオフ）：CPOは部品が減り設置・交換が容易とNVIDIAは主張するが 、着脱式は「現場で挿抜・交換できる」利点があり、CPOは固定実装ゆえの保守性 | E-0010 | fact | NVIDIA CPO requires fewer components and is much easier to install and replace than pluggable transceivers | 支持 | 引用は当該事実を支持 |
| 45 | report.md:L61 | ここは主張の裏取りが弱く、周回2で第三者情報が要る 。 | E-0010 | fact | NVIDIA CPO requires fewer components and is much easier to install and replace than pluggable transceivers | 支持 | 引用は当該事実を支持 |
| 46 | report.md:L65 | ** レーザーはLumentumが別部品として供給し 、パッケージには36の「レーザ入力（laser inputs）」として光を差し込む構成である 。 | E-0013 | fact | with Lumentum providing lasers for the Spectrum-X product and Coherent collaborating on silicon photonics | 支持 | 引用は当該事実を支持 |
| 47 | report.md:L65 | ** レーザーはLumentumが別部品として供給し 、パッケージには36の「レーザ入力（laser inputs）」として光を差し込む構成である 。 | E-0014 | fact | combines 18 silicon photonics engines, enabling 324 optical connections and 288 data links from 36 laser inputs | 支持 | 引用は当該事実を支持 |
| 48 | report.md:L65 | チップ上で行うのは光の点滅（変調）で、方式はマイクロリング変調器（MRM＝微小な輪で光を変調する素子）。 | E-0015 | fact | It is the world's first 1.6 Tb/s CPO, based on a technology called a micro ring modulator (MRM). It is completely built | 支持 | 引用は当該事実を支持 |
| 49 | report.md:L67 | メンブレン（薄膜）化合物半導体という技術で半導体レーザーを薄膜状に作り、シリコンフォトニクス回路の上に一体集積する 。 | E-0017 | fact | 「メンブレン化合物半導体技術」は半導体レーザなどを薄膜状に作製する技術で、低消費電力かつ高速な動作を実現でき、シリコンフォトニクス回路上にも作製することができます。 | 支持 | 引用は当該事実を支持 |
| 50 | report.md:L67 | 実際にシリコン基板上へ薄膜レーザーと光導波路を一体化し、1チップから16ポート出力する試作を示している 。 | E-0018 | fact | シリコン基板上にメンブレン化合物半導体からなるレーザとSiOxからなる光導波路を一体集積することで、1つのチップの片端面から16ポートでの出力を実現しています。 | 支持 | 引用は当該事実を支持 |
| 51 | report.md:L67 | ただしこのレーザー内蔵の光チップレットは**IOWN3.0世代での使用が目標**で、時間軸としては先である 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 | 引用は当該事実を支持 |
| 52 | report.md:L69 | ただし近未来の量産（NVIDIA・2026年）は外部光源方式で、発光内蔵は最後の段階に置かれている 。 | E-0013 | fact | with Lumentum providing lasers for the Spectrum-X product and Coherent collaborating on silicon photonics | 支持 | 引用は当該事実を支持 |
| 53 | report.md:L69 | ただし近未来の量産（NVIDIA・2026年）は外部光源方式で、発光内蔵は最後の段階に置かれている 。 | E-0017 | fact | 「メンブレン化合物半導体技術」は半導体レーザなどを薄膜状に作製する技術で、低消費電力かつ高速な動作を実現でき、シリコンフォトニクス回路上にも作製することができます。 | 支持 | 引用は当該事実を支持 |
| 54 | report.md:L69 | ただし近未来の量産（NVIDIA・2026年）は外部光源方式で、発光内蔵は最後の段階に置かれている 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 | 引用は当該事実を支持 |
| 55 | report.md:L71 | このため発光の集積は変調・受光の集積より難所が多い、と考えられる 。 | E-0017 | fact | 「メンブレン化合物半導体技術」は半導体レーザなどを薄膜状に作製する技術で、低消費電力かつ高速な動作を実現でき、シリコンフォトニクス回路上にも作製することができます。 | 支持 | 引用は当該事実を支持 |
| 56 | report.md:L75 | **どちらが優れているかではなく、狙う場所と時間軸が異なる** 。 | E-0002 | fact | integrating co-packaged optics (CPO) directly onto the ASIC, overcoming the limits of electrical signaling in large-scal | 支持 | 引用は当該事実を支持 |
| 57 | report.md:L75 | **どちらが優れているかではなく、狙う場所と時間軸が異なる** 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 | 引用は当該事実を支持 |
| 58 | report.md:L79 | - 標的レイヤー：NVIDIAはまずスイッチ（スケールアウト網）にCPOを入れる 。 | E-0002 | fact | integrating co-packaged optics (CPO) directly onto the ASIC, overcoming the limits of electrical signaling in large-scal | 支持 | 引用は当該事実を支持 |
| 59 | report.md:L79 | NTTはLSI直近→チップ間→最終的にチップ内まで光化を掲げる 。 | E-0018 | fact | シリコン基板上にメンブレン化合物半導体からなるレーザとSiOxからなる光導波路を一体集積することで、1つのチップの片端面から16ポートでの出力を実現しています。 | 支持 | 引用は当該事実を支持 |
| 60 | report.md:L79 | NTTはLSI直近→チップ間→最終的にチップ内まで光化を掲げる 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 | 引用は当該事実を支持 |
| 61 | report.md:L80 | - 発光レーザー：NVIDIA＝外部光源 、NTT＝薄膜レーザー内蔵 。 | E-0013 | fact | with Lumentum providing lasers for the Spectrum-X product and Coherent collaborating on silicon photonics | 支持 | 引用は当該事実を支持 |
| 62 | report.md:L80 | - 発光レーザー：NVIDIA＝外部光源 、NTT＝薄膜レーザー内蔵 。 | E-0014 | fact | combines 18 silicon photonics engines, enabling 324 optical connections and 288 data links from 36 laser inputs | 支持 | 引用は当該事実を支持 |
| 63 | report.md:L80 | - 発光レーザー：NVIDIA＝外部光源 、NTT＝薄膜レーザー内蔵 。 | E-0017 | fact | 「メンブレン化合物半導体技術」は半導体レーザなどを薄膜状に作製する技術で、低消費電力かつ高速な動作を実現でき、シリコンフォトニクス回路上にも作製することができます。 | 支持 | 引用は当該事実を支持 |
| 64 | report.md:L80 | - 発光レーザー：NVIDIA＝外部光源 、NTT＝薄膜レーザー内蔵 。 | E-0018 | fact | シリコン基板上にメンブレン化合物半導体からなるレーザとSiOxからなる光導波路を一体集積することで、1つのチップの片端面から16ポートでの出力を実現しています。 | 支持 | 引用は当該事実を支持 |
| 65 | report.md:L81 | - 時間軸：NVIDIAは2026年にスイッチCPOを量産予定 。 | E-0020 | fact | With commercial availability for NVIDIA Quantum-X InfiniBand switches set for early 2026 and Spectrum-X Ethernet switche | 支持 | 引用は当該事実を支持 |
| 66 | report.md:L81 | NTTはIOWN1.0が2023年、レーザー内蔵はIOWN3.0世代 。 | E-0022 | fact | IOWN1.0サービスは2023年度に開始しており、IOWN2.0、IOWN3.0が順次展開される予定です。 | 支持 | 引用は当該事実を支持 |
| 67 | report.md:L81 | NTTはIOWN1.0が2023年、レーザー内蔵はIOWN3.0世代 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 | 引用は当該事実を支持 |
| 68 | report.md:L83 | どちらが標準になるかは現時点で判断材料が不足する 。 | E-0002 | fact | integrating co-packaged optics (CPO) directly onto the ASIC, overcoming the limits of electrical signaling in large-scal | 支持 | 引用は当該事実を支持 |
| 69 | report.md:L83 | どちらが標準になるかは現時点で判断材料が不足する 。 | E-0020 | fact | With commercial availability for NVIDIA Quantum-X InfiniBand switches set for early 2026 and Spectrum-X Ethernet switche | 支持 | 引用は当該事実を支持 |
| 70 | report.md:L83 | どちらが標準になるかは現時点で判断材料が不足する 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 | 引用は当該事実を支持 |
| 71 | report.md:L87 | - 銅（電気ケーブル）は消えない：スケールアップ（GPU間最短）は現在ケーブル接続で 、短距離では銅が残る。 | E-0030 | fact | NVLink Switch trays and NVLink spine of 5,000 cables form a single all-to-all topology so any GPU can communicate with a | 支持 | 引用は当該事実を支持 |
| 72 | report.md:L87 | 銅が不利になるのは800Gb/s級を延伸距離で送る場合で、そこで初めて光が必須になる 。 | E-0031 | fact | which makes copper impractical at speeds like 800 Gb/s, so optical connections are required for nearly every server-to-s | 支持 | 引用は当該事実を支持 |
| 73 | report.md:L88 | - 近接実装光（NPO）：CPOの立ち上げ課題への"保険"として、パッケージのすぐ隣に光を置くNPOも業界で動いている、との指摘がある（関連記事見出しベースで確 | E-0032 | opinion | Near-packaged optics (NPO) gains ground as the industry hedges against CPO's growing pains | 支持 | 引用は当該事実を支持 |
| 74 | report.md:L101 | H3について：周回2で光源供給・ファイバ結合・実装検査の各層に担い手と各社の投資・自動化を確認し （§10〜§12, 図F-07）、支持と判定した。 | E-0036 | fact | NVIDIA is investing $2 billion in Lumentum to support R&D, future capacity and operations as the company builds out its | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 75 | report.md:L101 | H3について：周回2で光源供給・ファイバ結合・実装検査の各層に担い手と各社の投資・自動化を確認し （§10〜§12, 図F-07）、支持と判定した。 | E-0042 | fact | complete faceplate-to-chip optical assemblies for TH6-Davisson systems | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 76 | report.md:L101 | H3について：周回2で光源供給・ファイバ結合・実装検査の各層に担い手と各社の投資・自動化を確認し （§10〜§12, 図F-07）、支持と判定した。 | E-0056 | fact | introducing advanced automation, such as robotics, into the assembly, packaging, and inspection processes | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 77 | report.md:L105 | - 「発光レーザー部品がチップ内部へ入り込む方向」という見立ては、大きな方向としては妥当 。 | E-0017 | fact | 「メンブレン化合物半導体技術」は半導体レーザなどを薄膜状に作製する技術で、低消費電力かつ高速な動作を実現でき、シリコンフォトニクス回路上にも作製することができます。 | 支持 | 引用は当該事実を支持 |
| 78 | report.md:L105 | - 「発光レーザー部品がチップ内部へ入り込む方向」という見立ては、大きな方向としては妥当 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 | 引用は当該事実を支持 |
| 79 | report.md:L105 | ただし2026年の主役はスイッチのパッケージ内CPOで、そこでも発光は外部光源であり 、演算チップ（GPU）至近の光化・発光内蔵は"次の段階"に置かれている 。 | E-0002 | fact | integrating co-packaged optics (CPO) directly onto the ASIC, overcoming the limits of electrical signaling in large-scal | 支持 | 引用は当該事実を支持 |
| 80 | report.md:L105 | ただし2026年の主役はスイッチのパッケージ内CPOで、そこでも発光は外部光源であり 、演算チップ（GPU）至近の光化・発光内蔵は"次の段階"に置かれている 。 | E-0013 | fact | with Lumentum providing lasers for the Spectrum-X product and Coherent collaborating on silicon photonics | 支持 | 引用は当該事実を支持 |
| 81 | report.md:L105 | ただし2026年の主役はスイッチのパッケージ内CPOで、そこでも発光は外部光源であり 、演算チップ（GPU）至近の光化・発光内蔵は"次の段階"に置かれている 。 | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 支持 | 引用は当該事実を支持 |
| 82 | report.md:L105 | ただし2026年の主役はスイッチのパッケージ内CPOで、そこでも発光は外部光源であり 、演算チップ（GPU）至近の光化・発光内蔵は"次の段階"に置かれている 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 | 引用は当該事実を支持 |
| 83 | report.md:L106 | - 監視すべき節目：①NVIDIAのスケールアップ（NVLink）が光化に踏み出す時期  ②GPU同一パッケージへの発光内蔵の量産化 ③NTT IOWN3.0関 | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 84 | report.md:L106 | - 監視すべき節目：①NVIDIAのスケールアップ（NVLink）が光化に踏み出す時期  ②GPU同一パッケージへの発光内蔵の量産化 ③NTT IOWN3.0関 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 85 | report.md:L114 | - 事実：発光光源（外部レーザ）は独立した供給層で、LumentumのELSFPは複数の光エンジンで1つの高出力レーザを共有させ、CWレーザをスイッチ/ASIC | E-0034 | fact | the ELSFP enables multiple silicon photonics (SiPh) optical engines to share a single, high-power laser source | 支持 | 引用は当該事実を支持 |
| 86 | report.md:L114 | レーザはInP（リン化インジウム）基板上に作られる 。 | E-0035 | fact | Built on our proven indium phosphide (InP) platform | 支持 | 引用は当該事実を支持 |
| 87 | report.md:L115 | - 事実：NVIDIAはこの光源供給を確保するため、Lumentumへ2 billion ドルを出資し、米国内の新工場で製造能力を拡張させる 。 | E-0036 | fact | NVIDIA is investing $2 billion in Lumentum to support R&D, future capacity and operations as the company builds out its | 支持 | 引用は当該事実を支持 |
| 88 | report.md:L115 | 合意には巨額の購入コミットメントと将来キャパシティ確保権が含まれる 。 | E-0037 | fact | The nonexclusive agreement includes an NVIDIA multibillion purchase commitment and future capacity access rights for adv | 支持 | 引用は当該事実を支持 |
| 89 | report.md:L116 | Broadcomの第三世代CPO「Davisson」は102.4 Tb/sで 、TSMC COUPEの光エンジンを基板レベル実装で異種集積し 、外部光源はNVI | E-0039 | fact | an unprecedented 102.4 terabits per second of optically enabled switching capacity | 支持 | 引用は当該事実を支持 |
| 90 | report.md:L116 | Broadcomの第三世代CPO「Davisson」は102.4 Tb/sで 、TSMC COUPEの光エンジンを基板レベル実装で異種集積し 、外部光源はNVI | E-0040 | fact | By heterogeneously integrating TSMC Compact Universal Photonic Engine (TSMC COUPE) technology-based optical engines with | 支持 | 引用は当該事実を支持 |
| 91 | report.md:L116 | Broadcomの第三世代CPO「Davisson」は102.4 Tb/sで 、TSMC COUPEの光エンジンを基板レベル実装で異種集積し 、外部光源はNVI | E-0041 | fact | Field-Replaceable ELSFP Laser Modules | 支持 | 引用は当該事実を支持 |
| 92 | report.md:L116 | Broadcomの第三世代CPO「Davisson」は102.4 Tb/sで 、TSMC COUPEの光エンジンを基板レベル実装で異種集積し 、外部光源はNVI | E-0042 | fact | complete faceplate-to-chip optical assemblies for TH6-Davisson systems | 支持 | 引用は当該事実を支持 |
| 93 | report.md:L117 | - 事実：IOWN側はNTT Innovative Devicesが光エンジン・スイッチの設計製造とシステム統合の中核で 、PEC-2の供給網にBroadcom | E-0054 | fact | NTT Innovative Devices serves as the design and manufacturing hub for the core optical engine and switch modules and coo | 支持 | 引用は当該事実を支持 |
| 94 | report.md:L117 | - 事実：IOWN側はNTT Innovative Devicesが光エンジン・スイッチの設計製造とシステム統合の中核で 、PEC-2の供給網にBroadcom | E-0053 | fact | we have established partnerships across the global supply chain, including with Broadcom in the United States and Accton | 支持 | 引用は当該事実を支持 |
| 95 | report.md:L117 | PEC-2は発光（レーザダイオード）を内蔵する光エンジンで 、電気配線を約300mmから約30mmへ短縮する 。 | E-0057 | fact | A PEC device is an integrated package containing all the functions needed to convert signals between light and electrici | 支持 | 引用は当該事実を支持 |
| 96 | report.md:L117 | PEC-2は発光（レーザダイオード）を内蔵する光エンジンで 、電気配線を約300mmから約30mmへ短縮する 。 | E-0052 | fact | At roughly 300 mm, this long electrical wiring was a major contributor to increased power consumption. In the PEC switch | 支持 | 引用は当該事実を支持 |
| 97 | report.md:L118 | TSMC COUPEをNVIDIAとBroadcomの双方が使い 、外部光源ELSFPも双方が採用し 、BroadcomはNTT IOWNのPEC-2にも関与す | E-0040 | fact | By heterogeneously integrating TSMC Compact Universal Photonic Engine (TSMC COUPE) technology-based optical engines with | 支持 | 引用は当該事実を支持 |
| 98 | report.md:L118 | TSMC COUPEをNVIDIAとBroadcomの双方が使い 、外部光源ELSFPも双方が採用し 、BroadcomはNTT IOWNのPEC-2にも関与す | E-0041 | fact | Field-Replaceable ELSFP Laser Modules | 支持 | 引用は当該事実を支持 |
| 99 | report.md:L118 | TSMC COUPEをNVIDIAとBroadcomの双方が使い 、外部光源ELSFPも双方が採用し 、BroadcomはNTT IOWNのPEC-2にも関与す | E-0053 | fact | we have established partnerships across the global supply chain, including with Broadcom in the United States and Accton | 支持 | 引用は当該事実を支持 |
| 100 | report.md:L118 | 同じ土俵の別レイヤー、というより供給網は地続き 。 | E-0040 | fact | By heterogeneously integrating TSMC Compact Universal Photonic Engine (TSMC COUPE) technology-based optical engines with | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 101 | report.md:L118 | 同じ土俵の別レイヤー、というより供給網は地続き 。 | E-0041 | fact | Field-Replaceable ELSFP Laser Modules | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 102 | report.md:L118 | 同じ土俵の別レイヤー、というより供給網は地続き 。 | E-0053 | fact | we have established partnerships across the global supply chain, including with Broadcom in the United States and Accton | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 103 | report.md:L119 | NVIDIAが光源供給の確保に出資 、Corningがファイバ結合を専任提供 、NTTが組立・パッケージ・検査へロボット自動化を導入 、という各社の行動が根拠 | E-0036 | fact | NVIDIA is investing $2 billion in Lumentum to support R&D, future capacity and operations as the company builds out its | 支持 | 引用は当該事実を支持 |
| 104 | report.md:L119 | NVIDIAが光源供給の確保に出資 、Corningがファイバ結合を専任提供 、NTTが組立・パッケージ・検査へロボット自動化を導入 、という各社の行動が根拠 | E-0037 | fact | The nonexclusive agreement includes an NVIDIA multibillion purchase commitment and future capacity access rights for adv | 支持 | 引用は当該事実を支持 |
| 105 | report.md:L119 | NVIDIAが光源供給の確保に出資 、Corningがファイバ結合を専任提供 、NTTが組立・パッケージ・検査へロボット自動化を導入 、という各社の行動が根拠 | E-0042 | fact | complete faceplate-to-chip optical assemblies for TH6-Davisson systems | 支持 | 引用は当該事実を支持 |
| 106 | report.md:L119 | NVIDIAが光源供給の確保に出資 、Corningがファイバ結合を専任提供 、NTTが組立・パッケージ・検査へロボット自動化を導入 、という各社の行動が根拠 | E-0056 | fact | introducing advanced automation, such as robotics, into the assembly, packaging, and inspection processes | 支持 | 引用は当該事実を支持 |
| 107 | report.md:L127 | 本周回で担い手が確認できたのは、①光源=Lumentum・Coherent 、②材料=InP基板 、③光エンジン=TSMC COUPE／（IOWN側）NTT I | E-0034 | fact | the ELSFP enables multiple silicon photonics (SiPh) optical engines to share a single, high-power laser source | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 108 | report.md:L127 | 本周回で担い手が確認できたのは、①光源=Lumentum・Coherent 、②材料=InP基板 、③光エンジン=TSMC COUPE／（IOWN側）NTT I | E-0036 | fact | NVIDIA is investing $2 billion in Lumentum to support R&D, future capacity and operations as the company builds out its | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 109 | report.md:L127 | 本周回で担い手が確認できたのは、①光源=Lumentum・Coherent 、②材料=InP基板 、③光エンジン=TSMC COUPE／（IOWN側）NTT I | E-0035 | fact | Built on our proven indium phosphide (InP) platform | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 110 | report.md:L127 | 本周回で担い手が確認できたのは、①光源=Lumentum・Coherent 、②材料=InP基板 、③光エンジン=TSMC COUPE／（IOWN側）NTT I | E-0040 | fact | By heterogeneously integrating TSMC Compact Universal Photonic Engine (TSMC COUPE) technology-based optical engines with | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 111 | report.md:L127 | 本周回で担い手が確認できたのは、①光源=Lumentum・Coherent 、②材料=InP基板 、③光エンジン=TSMC COUPE／（IOWN側）NTT I | E-0054 | fact | NTT Innovative Devices serves as the design and manufacturing hub for the core optical engine and switch modules and coo | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 112 | report.md:L127 | 本周回で担い手が確認できたのは、①光源=Lumentum・Coherent 、②材料=InP基板 、③光エンジン=TSMC COUPE／（IOWN側）NTT I | E-0049 | fact | Optical communication/interconnect has continually scaled down in distance while moving closer to the ASIC | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 113 | report.md:L127 | 本周回で担い手が確認できたのは、①光源=Lumentum・Coherent 、②材料=InP基板 、③光エンジン=TSMC COUPE／（IOWN側）NTT I | E-0042 | fact | complete faceplate-to-chip optical assemblies for TH6-Davisson systems | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 114 | report.md:L127 | 本周回で担い手が確認できたのは、①光源=Lumentum・Coherent 、②材料=InP基板 、③光エンジン=TSMC COUPE／（IOWN側）NTT I | E-0039 | fact | an unprecedented 102.4 terabits per second of optically enabled switching capacity | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 115 | report.md:L127 | 本周回で担い手が確認できたのは、①光源=Lumentum・Coherent 、②材料=InP基板 、③光エンジン=TSMC COUPE／（IOWN側）NTT I | E-0056 | fact | introducing advanced automation, such as robotics, into the assembly, packaging, and inspection processes | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 116 | report.md:L127 | 本周回で担い手が確認できたのは、①光源=Lumentum・Coherent 、②材料=InP基板 、③光エンジン=TSMC COUPE／（IOWN側）NTT I | E-0047 | fact | a lack of standards for connecting the optical modules is slowing adoption | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 117 | report.md:L129 | 補足：Amkor（実装大手）は「光インターコネクトは距離を縮めながらASICへ継続的に近づいてきた」と述べており 、周回1の仮説H1（実装位置が段階的にチップへ | E-0049 | fact | Optical communication/interconnect has continually scaled down in distance while moving closer to the ASIC | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 118 | report.md:L135 | 各社の「お金と手間のかけ方」を見ると、律速は特定の一点ではなく、光源供給と実装・検査に分散している 。 | E-0036 | fact | NVIDIA is investing $2 billion in Lumentum to support R&D, future capacity and operations as the company builds out its | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 119 | report.md:L135 | 各社の「お金と手間のかけ方」を見ると、律速は特定の一点ではなく、光源供給と実装・検査に分散している 。 | E-0042 | fact | complete faceplate-to-chip optical assemblies for TH6-Davisson systems | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 120 | report.md:L135 | 各社の「お金と手間のかけ方」を見ると、律速は特定の一点ではなく、光源供給と実装・検査に分散している 。 | E-0056 | fact | introducing advanced automation, such as robotics, into the assembly, packaging, and inspection processes | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 121 | report.md:L135 | NVIDIAは光源（レーザ）の確保のためにLumentumへ出資し新工場を作らせ 、購入コミットメントと将来キャパシティ確保権まで押さえた 。 | E-0036 | fact | NVIDIA is investing $2 billion in Lumentum to support R&D, future capacity and operations as the company builds out its | 支持 | 引用は当該事実を支持 |
| 122 | report.md:L135 | NVIDIAは光源（レーザ）の確保のためにLumentumへ出資し新工場を作らせ 、購入コミットメントと将来キャパシティ確保権まで押さえた 。 | E-0037 | fact | The nonexclusive agreement includes an NVIDIA multibillion purchase commitment and future capacity access rights for adv | 支持 | 引用は当該事実を支持 |
| 123 | report.md:L135 | ファイバ結合はCorningがfaceplate-to-chipのアセンブリを専任的に供給する 。 | E-0042 | fact | complete faceplate-to-chip optical assemblies for TH6-Davisson systems | 支持 | 引用は当該事実を支持 |
| 124 | report.md:L135 | NTTは組立・パッケージ・検査の工程にロボット自動化を入れ、月5000個/ラインの能力を増強中である 。 | E-0055 | fact | NTT Innovative Devices is currently building a production capability of 5000 optical engines per month per manufacturing | 支持 | 引用は当該事実を支持 |
| 125 | report.md:L135 | NTTは組立・パッケージ・検査の工程にロボット自動化を入れ、月5000個/ラインの能力を増強中である 。 | E-0056 | fact | introducing advanced automation, such as robotics, into the assembly, packaging, and inspection processes | 支持 | 引用は当該事実を支持 |
| 126 | report.md:L135 | さらに、光エンジンをスイッチと同梱する統合設計は、着脱式に内在する製造・検査のばらつきの多くを取り除く 。 | E-0043 | fact | This highly integrated design eliminates many of the sources of manufacturing and test variability inherent in pluggable | 支持 | 引用は当該事実を支持 |
| 127 | report.md:L137 | 仮説H3は支持される 。 | E-0036 | fact | NVIDIA is investing $2 billion in Lumentum to support R&D, future capacity and operations as the company builds out its | 支持 | 引用は当該事実を支持 |
| 128 | report.md:L137 | 仮説H3は支持される 。 | E-0042 | fact | complete faceplate-to-chip optical assemblies for TH6-Davisson systems | 支持 | 引用は当該事実を支持 |
| 129 | report.md:L137 | 仮説H3は支持される 。 | E-0056 | fact | introducing advanced automation, such as robotics, into the assembly, packaging, and inspection processes | 支持 | 引用は当該事実を支持 |
| 130 | report.md:L137 | 仮説H3は支持される 。 | E-0043 | fact | This highly integrated design eliminates many of the sources of manufacturing and test variability inherent in pluggable | 支持 | 引用は当該事実を支持 |
| 131 | report.md:L137 | NVIDIA自身も、製造・組立・パッケージ・検査を第三者に依存すると開示している 。 | E-0038 | fact | NVIDIA's reliance on third parties to manufacture, assemble, package and test NVIDIA's products | 支持 | 引用は当該事実を支持 |
| 132 | report.md:L143 | 第一に、TSMC COUPE（光エンジンの製造基盤）はNVIDIA（周回1 E-0016）とBroadcom（Davisson）の双方が使う 。 | E-0040 | fact | By heterogeneously integrating TSMC Compact Universal Photonic Engine (TSMC COUPE) technology-based optical engines with | 支持 | 引用は当該事実を支持 |
| 133 | report.md:L143 | 第二に、外部光源ELSFPはNVIDIAだけでなくBroadcomのCPOも採用する 。 | E-0041 | fact | Field-Replaceable ELSFP Laser Modules | 支持 | 引用は当該事実を支持 |
| 134 | report.md:L143 | 第三に、Broadcomは自陣営のCPO（Davisson）と、NTT IOWNのPEC-2の供給網の双方に関与する 。 | E-0039 | fact | an unprecedented 102.4 terabits per second of optically enabled switching capacity | 支持 | 引用は当該事実を支持 |
| 135 | report.md:L143 | 第三に、Broadcomは自陣営のCPO（Davisson）と、NTT IOWNのPEC-2の供給網の双方に関与する 。 | E-0053 | fact | we have established partnerships across the global supply chain, including with Broadcom in the United States and Accton | 支持 | 引用は当該事実を支持 |
| 136 | report.md:L143 | 加えてNTT自身が、光配線の必要性の裏づけとしてBroadcom Tomahawk 6を引用している 。 | E-0059 | fact | Broadcom's Tomahawk 6 large-scale integrated circuit, which is used in datacenter switches, already processes 102 Tbit/s | 支持 | 引用は当該事実を支持 |
| 137 | report.md:L145 | 推論：したがって「NVIDIA陣営 vs IOWN陣営」は、標的レイヤー・時間軸では別（周回1の結論）だが、部品・製造基盤・企業の面では地続きで、特にBroad | E-0040 | fact | By heterogeneously integrating TSMC Compact Universal Photonic Engine (TSMC COUPE) technology-based optical engines with | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 138 | report.md:L145 | 推論：したがって「NVIDIA陣営 vs IOWN陣営」は、標的レイヤー・時間軸では別（周回1の結論）だが、部品・製造基盤・企業の面では地続きで、特にBroad | E-0053 | fact | we have established partnerships across the global supply chain, including with Broadcom in the United States and Accton | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 139 | report.md:L145 | 推論：したがって「NVIDIA陣営 vs IOWN陣営」は、標的レイヤー・時間軸では別（周回1の結論）だが、部品・製造基盤・企業の面では地続きで、特にBroad | E-0059 | fact | Broadcom's Tomahawk 6 large-scale integrated circuit, which is used in datacenter switches, already processes 102 Tbit/s | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 140 | report.md:L145 | 標準になりつつあるのがどちらか、という問いは、供給網が共通である以上「どちらか一方が総取り」よりも「同じ部品群の上で用途別に併存」の可能性がある 。 | E-0040 | fact | By heterogeneously integrating TSMC Compact Universal Photonic Engine (TSMC COUPE) technology-based optical engines with | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 141 | report.md:L145 | 標準になりつつあるのがどちらか、という問いは、供給網が共通である以上「どちらか一方が総取り」よりも「同じ部品群の上で用途別に併存」の可能性がある 。 | E-0044 | fact | it seamlessly interconnects with DR-based transceivers as well as LPO and CPO optical interconnects running at 200 Gbps | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 142 | report.md:L151 | 周回1で積み残したLPO（線形着脱光）は、モジュールからDSP（信号を整える処理チップ）機能だけをスイッチ側へ移し、電気信号で直接モジュールを駆動する着脱式であ | E-0045 | fact | moves only the DSP functionality out of the pluggable module and places it into a top of rack (ToR) switch so that elect | 支持 | 引用は当該事実を支持 |
| 143 | report.md:L151 | CPOより省電力の効果は小さいが、熱の影響（光信号のドリフト）に強いという利点がある 。 | E-0046 | fact | Although LPO saves less power than CPO, one advantage is that it provides better protection from thermal effects | 支持 | 引用は当該事実を支持 |
| 144 | report.md:L151 | 担い手・仕組みづくりはOIFとLPO-MSAが中心で、モジュール接続の標準が整備途上なことが普及の壁になっている 。 | E-0047 | fact | a lack of standards for connecting the optical modules is slowing adoption | 支持 | 引用は当該事実を支持 |
| 145 | report.md:L151 | 時間軸では、LPOはCPOに先行して商用化されるとの見通しである 。 | E-0048 | forecast | the newer LPO is likely to be commercialized ahead of CPO | 支持 | 引用は当該事実を支持 |
| 146 | report.md:L151 | 実際、BroadcomのCPO（Davisson）もLPO/CPOと相互接続する設計で 、両者は当面併存し得る。 | E-0044 | fact | it seamlessly interconnects with DR-based transceivers as well as LPO and CPO optical interconnects running at 200 Gbps | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 147 | report.md:L155 | 周回1で読み取れずにいたIOWNの最新商用段階（PEC-2）を、NTT公式（R&D FORUM 2025基調講演）で確認できた （依頼R-001は解消）。 | E-0050 | fact | The optical communication switch (PEC switch) incorporates 16 PEC-2 devices, can transmit 102.4 Tbit/s | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 148 | report.md:L155 | PEC-2は発光（レーザダイオード）・レーザドライバ・フォトダイオード・電気アンプを1パッケージに内蔵した光エンジンで 、16個を束ねたPECスイッチは102. | E-0057 | fact | A PEC device is an integrated package containing all the functions needed to convert signals between light and electrici | 支持 | 引用は当該事実を支持 |
| 149 | report.md:L155 | PEC-2は発光（レーザダイオード）・レーザドライバ・フォトダイオード・電気アンプを1パッケージに内蔵した光エンジンで 、16個を束ねたPECスイッチは102. | E-0050 | fact | The optical communication switch (PEC switch) incorporates 16 PEC-2 devices, can transmit 102.4 Tbit/s | 支持 | 引用は当該事実を支持 |
| 150 | report.md:L155 | 2026年度の商用提供を計画 。 | E-0051 | fact | commercial availability planned for fiscal year 2026 | 支持 | 引用は当該事実を支持 |
| 151 | report.md:L155 | 光エンジンとICを1枚のベースボードに載せ、電気配線を約300mmから約30mmへ短縮する 。 | E-0052 | fact | At roughly 300 mm, this long electrical wiring was a major contributor to increased power consumption. In the PEC switch | 支持 | 引用は当該事実を支持 |
| 152 | report.md:L155 | 担い手は、設計・製造とシステム統合の中核がNTT Innovative Devices 、供給網にBroadcom（米）とAccton（台湾）。 | E-0054 | fact | NTT Innovative Devices serves as the design and manufacturing hub for the core optical engine and switch modules and coo | 支持 | 引用は当該事実を支持 |
| 153 | report.md:L155 | 担い手は、設計・製造とシステム統合の中核がNTT Innovative Devices 、供給網にBroadcom（米）とAccton（台湾）。 | E-0053 | fact | we have established partnerships across the global supply chain, including with Broadcom in the United States and Accton | 支持 | 引用は当該事実を支持 |
| 154 | report.md:L155 | 生産能力は月5000個/ラインを構築中で、少なくとも三ラインへ拡張予定 。 | E-0055 | fact | NTT Innovative Devices is currently building a production capability of 5000 optical engines per month per manufacturing | 支持 | 引用は当該事実を支持 |
| 155 | report.md:L155 | 次のIOWN 3.0では、薄膜（メンブレン）デバイスの光チップレットでCPU/GPUのパッケージ間を光化し、2028年に商用サンプルを提供する計画である 。 | E-0058 | forecast | We expect to begin offering commercial samples in 2028 | 支持 | 引用は当該事実を支持 |
| 156 | report.md:L157 | NTTは発光を内蔵する方向（PEC-2で既に内蔵）だが、その内蔵は当面「ボード間（PEC-2）」までで、チップ間（PEC-3）は2028年サンプル、パッケージ内 | E-0057 | fact | A PEC device is an integrated package containing all the functions needed to convert signals between light and electrici | 支持 | 引用は当該事実を支持 |
| 157 | report.md:L157 | NTTは発光を内蔵する方向（PEC-2で既に内蔵）だが、その内蔵は当面「ボード間（PEC-2）」までで、チップ間（PEC-3）は2028年サンプル、パッケージ内 | E-0058 | forecast | We expect to begin offering commercial samples in 2028 | 支持 | 引用は当該事実を支持 |
| 158 | report.md:L161 | - Kenさんの想定に照らすと、「発光がチップへ入る」流れの担い手は、外部光源側ではLumentum/Coherent（NVIDIAが供給を確保）、内蔵側ではN | E-0036 | fact | NVIDIA is investing $2 billion in Lumentum to support R&D, future capacity and operations as the company builds out its | 支持 | 引用は当該事実を支持 |
| 159 | report.md:L161 | - Kenさんの想定に照らすと、「発光がチップへ入る」流れの担い手は、外部光源側ではLumentum/Coherent（NVIDIAが供給を確保）、内蔵側ではN | E-0054 | fact | NTT Innovative Devices serves as the design and manufacturing hub for the core optical engine and switch modules and coo | 支持 | 引用は当該事実を支持 |
| 160 | report.md:L161 | - Kenさんの想定に照らすと、「発光がチップへ入る」流れの担い手は、外部光源側ではLumentum/Coherent（NVIDIAが供給を確保）、内蔵側ではN | E-0057 | fact | A PEC device is an integrated package containing all the functions needed to convert signals between light and electrici | 支持 | 引用は当該事実を支持 |
| 161 | report.md:L162 | 両陣営の供給網がここで交差しており 、ここの能力・歩留まりが全体の律速になりやすい 。 | E-0040 | fact | By heterogeneously integrating TSMC Compact Universal Photonic Engine (TSMC COUPE) technology-based optical engines with | 支持 | 引用は当該事実を支持 |
| 162 | report.md:L162 | 両陣営の供給網がここで交差しており 、ここの能力・歩留まりが全体の律速になりやすい 。 | E-0053 | fact | we have established partnerships across the global supply chain, including with Broadcom in the United States and Accton | 支持 | 引用は当該事実を支持 |
| 163 | report.md:L162 | 両陣営の供給網がここで交差しており 、ここの能力・歩留まりが全体の律速になりやすい 。 | E-0043 | fact | This highly integrated design eliminates many of the sources of manufacturing and test variability inherent in pluggable | 支持 | 引用は当該事実を支持 |
| 164 | report.md:L162 | 両陣営の供給網がここで交差しており 、ここの能力・歩留まりが全体の律速になりやすい 。 | E-0056 | fact | introducing advanced automation, such as robotics, into the assembly, packaging, and inspection processes | 支持 | 引用は当該事実を支持 |
| 165 | report.md:L169 | - 性能値の多く（電力効率3.5倍・5倍、損失22dB→4dB、電力30W→9W）は**ベンダー（NVIDIA）自身が公表した値**であり、第三者の実測は本周回 | E-0007 | fact | They integrate optics innovations with 4x fewer lasers to deliver 3.5x more power efficiency, 63x greater signal integri | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 166 | report.md:L169 | - 性能値の多く（電力効率3.5倍・5倍、損失22dB→4dB、電力30W→9W）は**ベンダー（NVIDIA）自身が公表した値**であり、第三者の実測は本周回 | E-0008 | fact | NVIDIA CPO technology significantly reduces network power, enabling 5x better power efficiency over pluggable transceive | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 167 | report.md:L169 | - 性能値の多く（電力効率3.5倍・5倍、損失22dB→4dB、電力30W→9W）は**ベンダー（NVIDIA）自身が公表した値**であり、第三者の実測は本周回 | E-0003 | fact | Fiber connects directly with the optical engine that sits beside the ASIC, reducing electrical loss to only ~4 dB and sl | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 168 | report.md:L169 | - 性能値の多く（電力効率3.5倍・5倍、損失22dB→4dB、電力30W→9W）は**ベンダー（NVIDIA）自身が公表した値**であり、第三者の実測は本周回 | E-0005 | fact | This segmented journey incurs substantial electrical loss, up to 22 dB for 200 gigabit-per-second channels | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 169 | report.md:L169 | - 性能値の多く（電力効率3.5倍・5倍、損失22dB→4dB、電力30W→9W）は**ベンダー（NVIDIA）自身が公表した値**であり、第三者の実測は本周回 | E-0006 | fact | The result is a higher power draw (often 30W per interface) | 判断不能 | メタ/推論のため引用単体では判定保留 |
| 170 | report.md:L171 | ただし直近更新の製品ページ  とNVLink記事  で近時点を補っている。 | E-0021 | fact | With up to 409.6 terabits-per-second (Tb/s) bandwidth, Spectrum-X Ethernet Photonics enables massive generative AI workl | 支持 | 引用は当該事実を支持 |
| 171 | report.md:L171 | ただし直近更新の製品ページ  とNVLink記事  で近時点を補っている。 | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 支持 | 引用は当該事実を支持 |

（171件）

## 別セッションに貼るときの依頼文

```
この表の各行について、引用文が主張を支持しているかを判定してください。
レポート全体の文脈や、書き手の意図は考慮しないでください。
引用文だけを読んで、支持 / 部分的 / 不支持 / 判断不能 のいずれかを付け、
不支持・部分的の場合は理由を書いてください。
一般常識や業界知識で補って「支持」としないでください。
引用に書かれていないことは、書かれていないと扱います。
```

「このレポートは正しいですか」とは聞かないこと。
全体の妥当性を問うと、もっともらしさで判断されてしまう。

## 記入時の着眼点

- 主語・対象が入れ替わっていないか（別セグメント、別会社、別製品）
- 主張の向きが引用と逆になっていないか（肯定/否定）
- 単一時点の引用で、変化や傾向を語っていないか
- 会社予想・第三者見解を、事実として書いていないか
- 引用の一部だけを切り出して、条件や留保を落としていないか
