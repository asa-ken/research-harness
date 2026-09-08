SOURCE: Semiconductor Engineering — Linear Pluggable Optics Save Energy In Data Centers (Bryon Moyer)
URL: https://semiengineering.com/linear-pluggable-optics-save-energy-in-data-centers/
TIER: T5 (専門メディア。OIF/Synopsys/Amkor等の実名専門家コメントに基づく)
DATE: 2025-02-24
FETCHED: 2026-09-07

Linear pluggable optics (LPO) is garnering more attention as a way to quickly and efficiently move data in and out of server racks, but a lack of standards for connecting the optical modules is slowing adoption at a time when there is growing pressure to reduce power in data centers.

LPO is the newest of two approaches to solving the power wall problem in data centers. Co-packaged optics (CPO), a technology whose development precedes LPO, moves optics out of an octal small form-factor pluggable (OSFP) module and into the electrical-component package, eliminating the pluggable module. LPO, in contrast, moves only the DSP functionality out of the pluggable module and places it into a top of rack (ToR) switch so that electrical signals can directly drive the module.

Although LPO saves less power than CPO, one advantage is that it provides better protection from thermal effects, which can cause optical signals to drift, than CPO does.

[Amkor / Suresh Jayaraman] "Optical communication/interconnect has continually scaled down in distance while moving closer to the ASIC. We have seen the transition from long-haul to metro to local-area networks and then into the data center."

The DSP consumes roughly 50% of the power of the entire pluggable module. The promise of LPO is that the DSP in the module is eliminated; what remains is some basic equalization and a transimpedance amplifier (TIA).

[Synopsys / Priyank Shukla] "Broadcom has publicly shared that they have about 35% power saving [with LPO]." Most LPO implementations today are in closed systems. The challenge is interoperability: without the retiming function, mixing vendors becomes challenging.

Standards for interoperability: a draft LPO multi-source agreement (MSA); and the OIF has two projects — Common Electrical I/O – 112G-Linear (serves LPO, CPO, NPO) and Retimed TX Linear RX (RTLR). "The OIF initiated its linear project prior to the LPO MSA with the specific objective to define an electrical interface that would allow interoperable non-retimed optical modules."

pJ/bit (Andy Bechtolsheim, Arista, as quoted): 18 pJ/b for retimed, 12 pJ/b for RTLR, 6 pJ/b for non-retimed.

Ahead of, but not replacing, CPO: the newer LPO is likely to be commercialized ahead of CPO. "Linear CPO will definitely save more power than LPO as the channel between electrical and optical die is extremely small in CPO" (OIF team). LPO should initially run from a half to a full meter. Whether CPO will eventually take over is unclear.

Named entities: OIF (standards), LPO-MSA, Synopsys (SerDes/interface IP), Amkor Technology (advanced packaging), Promex (assembly), Arista (Bechtolsheim).
