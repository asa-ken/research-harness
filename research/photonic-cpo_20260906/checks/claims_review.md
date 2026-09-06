# 主張⇔引用 独立レビュー表

レポートを書いた者以外が記入する。引用文だけを読み、
その引用が主張を支持しているかを判断する（原文に戻ってもよい）。

判定: `支持` / `不支持` / `部分的` / `判断不能`

**不支持・部分的が1件でもあれば、レポートを修正してからGBをやり直す。**

| # | 箇所 | 主張 | 根拠 | 種別 | 引用（原文） | 判定 | コメント |
|---|---|---|---|---|---|---|---|
| 1 | report.md:L13 | - 事実：いまAIデータセンターで実際に製品化が進む光電融合は、**ネットワークの「スイッチ」に光を同梱する形（CPO＝スイッチのASICと同じパッケージに光変 | E-0002 | fact | integrating co-packaged optics (CPO) directly onto the ASIC, overcoming the limits of electrical signaling in large-scal | 支持 |  |
| 2 | report.md:L13 | - 事実：いまAIデータセンターで実際に製品化が進む光電融合は、**ネットワークの「スイッチ」に光を同梱する形（CPO＝スイッチのASICと同じパッケージに光変 | E-0020 | fact | With commercial availability for NVIDIA Quantum-X InfiniBand switches set for early 2026 and Spectrum-X Ethernet switche | 支持 |  |
| 3 | report.md:L13 | - 事実：いまAIデータセンターで実際に製品化が進む光電融合は、**ネットワークの「スイッチ」に光を同梱する形（CPO＝スイッチのASICと同じパッケージに光変 | E-0021 | fact | With up to 409.6 terabits-per-second (Tb/s) bandwidth, Spectrum-X Ethernet Photonics enables massive generative AI workl | 支持 |  |
| 4 | report.md:L14 | レーザーは外部の光源（Lumentumが供給）から「光の入力」としてパッケージへ差し込む構成で、チップ上ではもっぱら光の"点滅"（変調）と受光を行う 。 | E-0013 | fact | with Lumentum providing lasers for the Spectrum-X product and Coherent collaborating on silicon photonics | 支持 |  |
| 5 | report.md:L14 | レーザーは外部の光源（Lumentumが供給）から「光の入力」としてパッケージへ差し込む構成で、チップ上ではもっぱら光の"点滅"（変調）と受光を行う 。 | E-0014 | fact | combines 18 silicon photonics engines, enabling 324 optical connections and 288 data links from 36 laser inputs | 支持 | 『36 laser inputs』が、光を外から入力する外部光源構成を直接示す |
| 6 | report.md:L14 | レーザーは外部の光源（Lumentumが供給）から「光の入力」としてパッケージへ差し込む構成で、チップ上ではもっぱら光の"点滅"（変調）と受光を行う 。 | E-0015 | fact | It is the world's first 1.6 Tb/s CPO, based on a technology called a micro ring modulator (MRM). It is completely built  | 支持 | 『micro ring modulator (MRM)』でチップ側は変調を担うことを支持 |
| 7 | report.md:L15 | - 事実：**GPU同士の最短接続（スケールアップ／NVLink）は現在ケーブル（電気）**で、これを光化するのはNVIDIA自身が「将来のロードマップ」と位置 | E-0030 | fact | NVLink Switch trays and NVLink spine of 5,000 cables form a single all-to-all topology so any GPU can communicate with a | 支持 | 『5,000 cables』でスケールアップが現状は電気接続であることを示す |
| 8 | report.md:L15 | - 事実：**GPU同士の最短接続（スケールアップ／NVLink）は現在ケーブル（電気）**で、これを光化するのはNVIDIA自身が「将来のロードマップ」と位置 | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 支持 |  |
| 9 | report.md:L16 | 当面（〜2026年）はスイッチ層でのCPO＋外部光源が主流、という順序になる 。 | E-0004 | fact | The first generation is an optical engine for OSFP connectors, offering 1.6 Tb/s data transfer while reducing power cons | 支持 |  |
| 10 | report.md:L16 | 当面（〜2026年）はスイッチ層でのCPO＋外部光源が主流、という順序になる 。 | E-0013 | fact | with Lumentum providing lasers for the Spectrum-X product and Coherent collaborating on silicon photonics | 支持 |  |
| 11 | report.md:L16 | 当面（〜2026年）はスイッチ層でのCPO＋外部光源が主流、という順序になる 。 | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 支持 |  |
| 12 | report.md:L18 | ** 理由：一次資料（NVIDIA公式・NTT公式）で骨格は固いが、性能値の多く（電力効率3.5〜5倍など）は**ベンダー自身の主張で独立検証がなく** 、評価 | E-0007 | fact | They integrate optics innovations with 4x fewer lasers to deliver 3.5x more power efficiency, 63x greater signal integri | 支持 |  |
| 13 | report.md:L18 | ** 理由：一次資料（NVIDIA公式・NTT公式）で骨格は固いが、性能値の多く（電力効率3.5〜5倍など）は**ベンダー自身の主張で独立検証がなく** 、評価 | E-0008 | fact | NVIDIA CPO technology significantly reduces network power, enabling 5x better power efficiency over pluggable transceive | 支持 |  |
| 14 | report.md:L21 | - 現在は発光を外部光源に置きスイッチ層でCPO化する段階だが 、これが覆り、GPU（演算チップ）と同一パッケージに発光レーザーまで内蔵した量産品が近い将来（数 | E-0013 | fact | with Lumentum providing lasers for the Spectrum-X product and Coherent collaborating on silicon photonics | 支持 |  |
| 15 | report.md:L21 | - 現在は発光を外部光源に置きスイッチ層でCPO化する段階だが 、これが覆り、GPU（演算チップ）と同一パッケージに発光レーザーまで内蔵した量産品が近い将来（数 | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 支持 |  |
| 16 | report.md:L22 | - スケールアップ（GPU間最短）が現在ケーブル接続である状態  が長く続く、または逆に急速に光化すれば、時間軸の描像は変わる。 | E-0030 | fact | NVLink Switch trays and NVLink spine of 5,000 cables form a single all-to-all topology so any GPU can communicate with a | 支持 |  |
| 17 | report.md:L35 | 狙いは消費電力の削減  と、より遠く・より大量のデータ伝送 。 | E-0003 | fact | Fiber connects directly with the optical engine that sits beside the ASIC, reducing electrical loss to only ~4 dB and sl | 支持 |  |
| 18 | report.md:L35 | 狙いは消費電力の削減  と、より遠く・より大量のデータ伝送 。 | E-0025 | fact | the Tier 1 switch is relocated to the end of the row. This configuration dramatically increases the distance between ser | 支持 |  |
| 19 | report.md:L37 | いま製品化の主役である**CPO（Co-Packaged Optics＝同梱光）**とは、これまでスイッチ前面に"挿していた"着脱式の光モジュールを、**スイッ | E-0001 | fact | Replacing pluggable transceivers with silicon photonics on the same package as the ASIC, NVIDIA CPO innovations provide  | 支持 |  |
| 20 | report.md:L37 | いま製品化の主役である**CPO（Co-Packaged Optics＝同梱光）**とは、これまでスイッチ前面に"挿していた"着脱式の光モジュールを、**スイッ | E-0002 | fact | integrating co-packaged optics (CPO) directly onto the ASIC, overcoming the limits of electrical signaling in large-scal | 支持 |  |
| 21 | report.md:L37 | 置き換える対象は、着脱式トランシーバとその長い電気配線 。 | E-0003 | fact | Fiber connects directly with the optical engine that sits beside the ASIC, reducing electrical loss to only ~4 dB and sl | 支持 |  |
| 22 | report.md:L39 | この距離では電気配線で信号が保たず、光が必須になる、というのが駆動力である 。 | E-0025 | fact | the Tier 1 switch is relocated to the end of the row. This configuration dramatically increases the distance between ser | 支持 |  |
| 23 | report.md:L39 | Huang氏は、従来方式ではGPU1個あたり6個のトランシーバで180W・$6000かかり、100万GPUなら180メガワットに達すると説明している（数値はNV | E-0026 | fact | each of those GPUs would require six individual transceivers, meaning a power consumption of 180 Watts and a cost of $60 | 支持 |  |
| 24 | report.md:L43 | 光を電気に代える「境界」が、外側から内側へ段階的に寄っていく ――これが本調査の背骨である。 | E-0004 | fact | The first generation is an optical engine for OSFP connectors, offering 1.6 Tb/s data transfer while reducing power cons | 支持 |  |
| 25 | report.md:L43 | TSMCの光基盤「COUPE」は3段階で進むとされ、**第1=コネクタ用（着脱式相当、1.6Tb/s）→ 第2=パッケージ同梱CPO（6.4Tb/s、基板レベル | E-0004 | fact | The first generation is an optical engine for OSFP connectors, offering 1.6 Tb/s data transfer while reducing power cons | 支持 |  |
| 26 | report.md:L47 | NVIDIAの2026年の製品は、この第2段階（スイッチのパッケージ内CPO）に当たる 。 | E-0002 | fact | integrating co-packaged optics (CPO) directly onto the ASIC, overcoming the limits of electrical signaling in large-scal | 支持 |  |
| 27 | report.md:L47 | NVIDIAの2026年の製品は、この第2段階（スイッチのパッケージ内CPO）に当たる 。 | E-0020 | fact | With commercial availability for NVIDIA Quantum-X InfiniBand switches set for early 2026 and Spectrum-X Ethernet switche | 支持 |  |
| 28 | report.md:L47 | 第3段階（プロセッサ・パッケージ内）は計画として示されるが時期は確定的でない 。 | E-0004 | fact | The first generation is an optical engine for OSFP connectors, offering 1.6 Tb/s data transfer while reducing power cons | 支持 |  |
| 29 | report.md:L47 | そしてGPU同士の最短接続（スケールアップ）は、現状ケーブル接続で、光化は将来ロードマップである 。 | E-0030 | fact | NVLink Switch trays and NVLink spine of 5,000 cables form a single all-to-all topology so any GPU can communicate with a | 支持 |  |
| 30 | report.md:L47 | そしてGPU同士の最短接続（スケールアップ）は、現状ケーブル接続で、光化は将来ロードマップである 。 | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 支持 |  |
| 31 | report.md:L49 | 推論：したがって「光がチップに近づく」流れは実在するが、2026年時点の到達点はスイッチのパッケージ内までで、演算チップ（GPU）そのものへ光が入り込むのはこれ | E-0004 | fact | The first generation is an optical engine for OSFP connectors, offering 1.6 Tb/s data transfer while reducing power cons | 支持 |  |
| 32 | report.md:L49 | 推論：したがって「光がチップに近づく」流れは実在するが、2026年時点の到達点はスイッチのパッケージ内までで、演算チップ（GPU）そのものへ光が入り込むのはこれ | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 支持 |  |
| 33 | report.md:L49 | 推論：したがって「光がチップに近づく」流れは実在するが、2026年時点の到達点はスイッチのパッケージ内までで、演算チップ（GPU）そのものへ光が入り込むのはこれ | E-0030 | fact | NVLink Switch trays and NVLink spine of 5,000 cables form a single all-to-all topology so any GPU can communicate with a | 支持 |  |
| 34 | report.md:L53 | 集めた資料が繰り返し挙げる主戦場は**電力**で、その源泉は**電気配線での信号損失**である 。 | E-0003 | fact | Fiber connects directly with the optical engine that sits beside the ASIC, reducing electrical loss to only ~4 dB and sl | 支持 |  |
| 35 | report.md:L53 | 集めた資料が繰り返し挙げる主戦場は**電力**で、その源泉は**電気配線での信号損失**である 。 | E-0005 | fact | This segmented journey incurs substantial electrical loss, up to 22 dB for 200 gigabit-per-second channels | 支持 |  |
| 36 | report.md:L57 | 具体的には、着脱式では信号がASICから基板・コネクタを経て遠回りするため200Gb/sチャネルで22dBに達する電気損失が生じ、ポートあたり約30Wを消費する | E-0005 | fact | This segmented journey incurs substantial electrical loss, up to 22 dB for 200 gigabit-per-second channels | 支持 |  |
| 37 | report.md:L57 | 具体的には、着脱式では信号がASICから基板・コネクタを経て遠回りするため200Gb/sチャネルで22dBに達する電気損失が生じ、ポートあたり約30Wを消費する | E-0006 | fact | The result is a higher power draw (often 30W per interface) | 支持 |  |
| 38 | report.md:L57 | CPOでは光エンジンをASICの隣に置きファイバ直結にすることで、損失は約4dB、電力は9W程度まで抑えられるとされる 。 | E-0003 | fact | Fiber connects directly with the optical engine that sits beside the ASIC, reducing electrical loss to only ~4 dB and sl | 支持 |  |
| 39 | report.md:L57 | さらにCPOはDSP（信号を補正する処理チップ）リタイマーを省け、遅延低減にも効くという 。 | E-0009 | fact | NVIDIA CPO doesn't require digital signal processing (DSP) retimers, reducing network latency | 支持 |  |
| 40 | report.md:L59 | ただし電力効率の倍率（3.5倍、のち製品ページで5倍）はNVIDIA自身が公表した主張であり、第三者による実測は本周回では未取得である 。 | E-0007 | fact | They integrate optics innovations with 4x fewer lasers to deliver 3.5x more power efficiency, 63x greater signal integri | 支持 |  |
| 41 | report.md:L59 | ただし電力効率の倍率（3.5倍、のち製品ページで5倍）はNVIDIA自身が公表した主張であり、第三者による実測は本周回では未取得である 。 | E-0008 | fact | NVIDIA CPO technology significantly reduces network power, enabling 5x better power efficiency over pluggable transceive | 支持 |  |
| 42 | report.md:L59 | スケールアップ網の文脈でNVIDIAは、評価は「時間・電力・設置面積あたりのトークン処理量」で見るべきとし、実効性能・耐障害性・成熟度/サプライチェーンの3点を | E-0011 | fact | Delivered, full-system performance determines how many tokens can be processed and produced per unit time, power, and fa | 支持 |  |
| 43 | report.md:L59 | スケールアップ網の文脈でNVIDIAは、評価は「時間・電力・設置面積あたりのトークン処理量」で見るべきとし、実効性能・耐障害性・成熟度/サプライチェーンの3点を | E-0012 | fact | The Key Metrics for Scale-Up Networking in AI Factories | 支持 |  |
| 44 | report.md:L61 | 注意（トレードオフ）：CPOは部品が減り設置・交換が容易とNVIDIAは主張するが 、着脱式は「現場で挿抜・交換できる」利点があり、CPOは固定実装ゆえの保守性 | E-0010 | fact | NVIDIA CPO requires fewer components and is much easier to install and replace than pluggable transceivers | 支持 |  |
| 45 | report.md:L61 | ここは主張の裏取りが弱く、周回2で第三者情報が要る 。 | E-0010 | fact | NVIDIA CPO requires fewer components and is much easier to install and replace than pluggable transceivers | 判断不能 | NVIDIAの主張であり、第三者検証の要否という評価は引用単体では判定できない |
| 46 | report.md:L65 | ** レーザーはLumentumが別部品として供給し 、パッケージには36の「レーザ入力（laser inputs）」として光を差し込む構成である 。 | E-0013 | fact | with Lumentum providing lasers for the Spectrum-X product and Coherent collaborating on silicon photonics | 支持 |  |
| 47 | report.md:L65 | ** レーザーはLumentumが別部品として供給し 、パッケージには36の「レーザ入力（laser inputs）」として光を差し込む構成である 。 | E-0014 | fact | combines 18 silicon photonics engines, enabling 324 optical connections and 288 data links from 36 laser inputs | 支持 |  |
| 48 | report.md:L65 | チップ上で行うのは光の点滅（変調）で、方式はマイクロリング変調器（MRM＝微小な輪で光を変調する素子）。 | E-0015 | fact | It is the world's first 1.6 Tb/s CPO, based on a technology called a micro ring modulator (MRM). It is completely built  | 支持 |  |
| 49 | report.md:L67 | メンブレン（薄膜）化合物半導体という技術で半導体レーザーを薄膜状に作り、シリコンフォトニクス回路の上に一体集積する 。 | E-0017 | fact | 「メンブレン化合物半導体技術」は半導体レーザなどを薄膜状に作製する技術で、低消費電力かつ高速な動作を実現でき、シリコンフォトニクス回路上にも作製することができます。 | 支持 | 薄膜レーザをシリコンフォトニクス上に作製可能＝発光内蔵の方向を支持 |
| 50 | report.md:L67 | 実際にシリコン基板上へ薄膜レーザーと光導波路を一体化し、1チップから16ポート出力する試作を示している 。 | E-0018 | fact | シリコン基板上にメンブレン化合物半導体からなるレーザとSiOxからなる光導波路を一体集積することで、1つのチップの片端面から16ポートでの出力を実現しています。 | 支持 | シリコン基板上に薄膜レーザ＋導波路を一体集積、を直接示す |
| 51 | report.md:L67 | ただしこのレーザー内蔵の光チップレットは**IOWN3.0世代での使用が目標**で、時間軸としては先である 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 |  |
| 52 | report.md:L69 | ただし近未来の量産（NVIDIA・2026年）は外部光源方式で、発光内蔵は最後の段階に置かれている 。 | E-0013 | fact | with Lumentum providing lasers for the Spectrum-X product and Coherent collaborating on silicon photonics | 支持 |  |
| 53 | report.md:L69 | ただし近未来の量産（NVIDIA・2026年）は外部光源方式で、発光内蔵は最後の段階に置かれている 。 | E-0017 | fact | 「メンブレン化合物半導体技術」は半導体レーザなどを薄膜状に作製する技術で、低消費電力かつ高速な動作を実現でき、シリコンフォトニクス回路上にも作製することができます。 | 支持 |  |
| 54 | report.md:L69 | ただし近未来の量産（NVIDIA・2026年）は外部光源方式で、発光内蔵は最後の段階に置かれている 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 |  |
| 55 | report.md:L71 | このため発光の集積は変調・受光の集積より難所が多い、と考えられる 。 | E-0017 | fact | 「メンブレン化合物半導体技術」は半導体レーザなどを薄膜状に作製する技術で、低消費電力かつ高速な動作を実現でき、シリコンフォトニクス回路上にも作製することができます。 | 支持 |  |
| 56 | report.md:L75 | **どちらが優れているかではなく、狙う場所と時間軸が異なる** 。 | E-0002 | fact | integrating co-packaged optics (CPO) directly onto the ASIC, overcoming the limits of electrical signaling in large-scal | 支持 |  |
| 57 | report.md:L75 | **どちらが優れているかではなく、狙う場所と時間軸が異なる** 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 |  |
| 58 | report.md:L79 | - 標的レイヤー：NVIDIAはまずスイッチ（スケールアウト網）にCPOを入れる 。 | E-0002 | fact | integrating co-packaged optics (CPO) directly onto the ASIC, overcoming the limits of electrical signaling in large-scal | 支持 |  |
| 59 | report.md:L79 | NTTはLSI直近→チップ間→最終的にチップ内まで光化を掲げる 。 | E-0018 | fact | シリコン基板上にメンブレン化合物半導体からなるレーザとSiOxからなる光導波路を一体集積することで、1つのチップの片端面から16ポートでの出力を実現しています。 | 支持 |  |
| 60 | report.md:L79 | NTTはLSI直近→チップ間→最終的にチップ内まで光化を掲げる 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 |  |
| 61 | report.md:L80 | - 発光レーザー：NVIDIA＝外部光源 、NTT＝薄膜レーザー内蔵 。 | E-0013 | fact | with Lumentum providing lasers for the Spectrum-X product and Coherent collaborating on silicon photonics | 支持 |  |
| 62 | report.md:L80 | - 発光レーザー：NVIDIA＝外部光源 、NTT＝薄膜レーザー内蔵 。 | E-0014 | fact | combines 18 silicon photonics engines, enabling 324 optical connections and 288 data links from 36 laser inputs | 支持 |  |
| 63 | report.md:L80 | - 発光レーザー：NVIDIA＝外部光源 、NTT＝薄膜レーザー内蔵 。 | E-0017 | fact | 「メンブレン化合物半導体技術」は半導体レーザなどを薄膜状に作製する技術で、低消費電力かつ高速な動作を実現でき、シリコンフォトニクス回路上にも作製することができます。 | 支持 |  |
| 64 | report.md:L80 | - 発光レーザー：NVIDIA＝外部光源 、NTT＝薄膜レーザー内蔵 。 | E-0018 | fact | シリコン基板上にメンブレン化合物半導体からなるレーザとSiOxからなる光導波路を一体集積することで、1つのチップの片端面から16ポートでの出力を実現しています。 | 支持 |  |
| 65 | report.md:L81 | - 時間軸：NVIDIAは2026年にスイッチCPOを量産予定 。 | E-0020 | fact | With commercial availability for NVIDIA Quantum-X InfiniBand switches set for early 2026 and Spectrum-X Ethernet switche | 支持 |  |
| 66 | report.md:L81 | NTTはIOWN1.0が2023年、レーザー内蔵はIOWN3.0世代 。 | E-0022 | fact | IOWN1.0サービスは2023年度に開始しており、IOWN2.0、IOWN3.0が順次展開される予定です。 | 支持 | IOWN1.0=2023、2.0/3.0順次、と明記され時間軸を支持 |
| 67 | report.md:L81 | NTTはIOWN1.0が2023年、レーザー内蔵はIOWN3.0世代 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 |  |
| 68 | report.md:L83 | どちらが標準になるかは現時点で判断材料が不足する 。 | E-0002 | fact | integrating co-packaged optics (CPO) directly onto the ASIC, overcoming the limits of electrical signaling in large-scal | 支持 |  |
| 69 | report.md:L83 | どちらが標準になるかは現時点で判断材料が不足する 。 | E-0020 | fact | With commercial availability for NVIDIA Quantum-X InfiniBand switches set for early 2026 and Spectrum-X Ethernet switche | 支持 |  |
| 70 | report.md:L83 | どちらが標準になるかは現時点で判断材料が不足する 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 |  |
| 71 | report.md:L87 | - 銅（電気ケーブル）は消えない：スケールアップ（GPU間最短）は現在ケーブル接続で 、短距離では銅が残る。 | E-0030 | fact | NVLink Switch trays and NVLink spine of 5,000 cables form a single all-to-all topology so any GPU can communicate with a | 支持 |  |
| 72 | report.md:L87 | 銅が不利になるのは800Gb/s級を延伸距離で送る場合で、そこで初めて光が必須になる 。 | E-0031 | fact | which makes copper impractical at speeds like 800 Gb/s, so optical connections are required for nearly every server-to-s | 支持 | 銅は800Gb/s延伸で非現実的＝短距離では銅が残る、という含意を支持 |
| 73 | report.md:L88 | - 近接実装光（NPO）：CPOの立ち上げ課題への"保険"として、パッケージのすぐ隣に光を置くNPOも業界で動いている、との指摘がある（関連記事見出しベースで確 | E-0032 | opinion | Near-packaged optics (NPO) gains ground as the industry hedges against CPO's growing pains | 支持 |  |
| 74 | report.md:L105 | - 「発光レーザー部品がチップ内部へ入り込む方向」という見立ては、大きな方向としては妥当 。 | E-0017 | fact | 「メンブレン化合物半導体技術」は半導体レーザなどを薄膜状に作製する技術で、低消費電力かつ高速な動作を実現でき、シリコンフォトニクス回路上にも作製することができます。 | 支持 |  |
| 75 | report.md:L105 | - 「発光レーザー部品がチップ内部へ入り込む方向」という見立ては、大きな方向としては妥当 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 |  |
| 76 | report.md:L105 | ただし2026年の主役はスイッチのパッケージ内CPOで、そこでも発光は外部光源であり 、演算チップ（GPU）至近の光化・発光内蔵は"次の段階"に置かれている 。 | E-0002 | fact | integrating co-packaged optics (CPO) directly onto the ASIC, overcoming the limits of electrical signaling in large-scal | 支持 |  |
| 77 | report.md:L105 | ただし2026年の主役はスイッチのパッケージ内CPOで、そこでも発光は外部光源であり 、演算チップ（GPU）至近の光化・発光内蔵は"次の段階"に置かれている 。 | E-0013 | fact | with Lumentum providing lasers for the Spectrum-X product and Coherent collaborating on silicon photonics | 支持 |  |
| 78 | report.md:L105 | ただし2026年の主役はスイッチのパッケージ内CPOで、そこでも発光は外部光源であり 、演算チップ（GPU）至近の光化・発光内蔵は"次の段階"に置かれている 。 | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 支持 |  |
| 79 | report.md:L105 | ただし2026年の主役はスイッチのパッケージ内CPOで、そこでも発光は外部光源であり 、演算チップ（GPU）至近の光化・発光内蔵は"次の段階"に置かれている 。 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 |  |
| 80 | report.md:L106 | - 監視すべき節目：①NVIDIAのスケールアップ（NVLink）が光化に踏み出す時期  ②GPU同一パッケージへの発光内蔵の量産化 ③NTT IOWN3.0関 | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 支持 |  |
| 81 | report.md:L106 | - 監視すべき節目：①NVIDIAのスケールアップ（NVLink）が光化に踏み出す時期  ②GPU同一パッケージへの発光内蔵の量産化 ③NTT IOWN3.0関 | E-0023 | fact | 光チップレットおよびその中のキーデバイスであるメンブレン化合物半導体技術は、IOWN3.0の時代に使用することを目標としています。 | 支持 |  |
| 82 | report.md:L112 | - 性能値の多く（電力効率3.5倍・5倍、損失22dB→4dB、電力30W→9W）は**ベンダー（NVIDIA）自身が公表した値**であり、第三者の実測は本周回 | E-0007 | fact | They integrate optics innovations with 4x fewer lasers to deliver 3.5x more power efficiency, 63x greater signal integri | 支持 |  |
| 83 | report.md:L112 | - 性能値の多く（電力効率3.5倍・5倍、損失22dB→4dB、電力30W→9W）は**ベンダー（NVIDIA）自身が公表した値**であり、第三者の実測は本周回 | E-0008 | fact | NVIDIA CPO technology significantly reduces network power, enabling 5x better power efficiency over pluggable transceive | 支持 |  |
| 84 | report.md:L112 | - 性能値の多く（電力効率3.5倍・5倍、損失22dB→4dB、電力30W→9W）は**ベンダー（NVIDIA）自身が公表した値**であり、第三者の実測は本周回 | E-0003 | fact | Fiber connects directly with the optical engine that sits beside the ASIC, reducing electrical loss to only ~4 dB and sl | 支持 |  |
| 85 | report.md:L112 | - 性能値の多く（電力効率3.5倍・5倍、損失22dB→4dB、電力30W→9W）は**ベンダー（NVIDIA）自身が公表した値**であり、第三者の実測は本周回 | E-0005 | fact | This segmented journey incurs substantial electrical loss, up to 22 dB for 200 gigabit-per-second channels | 支持 |  |
| 86 | report.md:L112 | - 性能値の多く（電力効率3.5倍・5倍、損失22dB→4dB、電力30W→9W）は**ベンダー（NVIDIA）自身が公表した値**であり、第三者の実測は本周回 | E-0006 | fact | The result is a higher power draw (often 30W per interface) | 支持 |  |
| 87 | report.md:L114 | ただし直近更新の製品ページ  とNVLink記事  で近時点を補っている。 | E-0021 | fact | With up to 409.6 terabits-per-second (Tb/s) bandwidth, Spectrum-X Ethernet Photonics enables massive generative AI workl | 判断不能 | 引用は内容であり、鮮度（更新の新しさ）の主張は出版日メタ情報に依存し引用単体では判定できない |
| 88 | report.md:L114 | ただし直近更新の製品ページ  とNVLink記事  で近時点を補っている。 | E-0024 | fact | The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-pac | 判断不能 | 引用は内容であり、鮮度（更新の新しさ）の主張は出版日メタ情報に依存し引用単体では判定できない |

（88件）

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
