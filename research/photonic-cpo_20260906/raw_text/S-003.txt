# Scaling AI Factories with Co-Packaged Optics for Better Power Efficiency

By Ashkan Seyedi. Published Aug 18, 2025. Modified 2025-09-04. NVIDIA Technical Blog.

## How does AI factory infrastructure compare to traditional enterprise data centers?

In traditional enterprise data centers, Tier 1 switches are integrated within each server's rack, allowing direct copper connections to servers and minimizing both power and component complexity. This architecture sufficed for CPU-centric workloads with modest networking demands.

In contrast, modern AI factories pioneered by NVIDIA feature ultra-dense compute racks and thousands of GPUs that are architected to work together on a single job. These require max bandwidth and minimum latency across the entire data center, which lead to new topologies where the Tier 1 switch is relocated to the end of the row. This configuration dramatically increases the distance between servers and switches, making optical networking essential. As a result, power consumption and the number of optical components rise significantly, with optics now required for both NIC-to-switch and switch-to-switch connections.

## How do you optimize network reliability and power for AI factories?

Traditional network switches that utilize pluggable transceivers rely on multiple electrical interfaces. In these architectures, the data signal must traverse long electrical paths from the switch ASIC to the PCB, connectors and finally into the external transceiver before being converted to an optical signal. This segmented journey incurs substantial electrical loss, up to 22 dB for 200 gigabit-per-second channels, as illustrated in Figure 2 below. This amplifies the need for complex digital signal processing and multiple active components.

The result is a higher power draw (often 30W per interface), increased heat output, and a proliferation of potential failure points. The abundance of discrete modules and connections not only drives up system power and component count but directly undermines link reliability, creating ongoing operational challenges as AI deployments scale.

In contrast, switches with co-packaged optics (CPO) integrate the electro-optical conversion directly onto the switch package. Fiber connects directly with the optical engine that sits beside the ASIC, reducing electrical loss to only ~4 dB and slashing power use to as low as 9W. By streamlining the signal path and eliminating unnecessary interfaces, this design dramatically improves signal integrity, reliability, and energy efficiency. This is precisely what's required for high-density, high-performance AI factories.

## What do co-packaged optics bring to AI factories?

NVIDIA has designed CPO-based systems to meet unprecedented AI factory demands. By integrating optical engines directly onto the switch ASIC, the new NVIDIA Quantum-X Photonics and Spectrum-X Photonics will replace legacy pluggable transceivers.

## How Quantum-X Photonics marks the next generation of InfiniBand networking

This platform features:
- 115 Tb/s of switching capacity, supporting 144 ports at 800 Gb/s each
- 14.4 teraflops of in-network computing with the fourth generation of NVIDIA Scalable Hierarchical Aggregation Reduction Protocol (SHARP) technology
- Liquid cooling for superior thermal management
- Dedicated InfiniBand management ports for robust in-band control and monitoring

## How Spectrum-X Photonics enables massive scale Ethernet AI factories

The new Spectrum-X Photonics offerings include two liquid-cooled chasses based on the Spectrum-6 ASIC:
- Spectrum SN6810: 102.4 Tb/s bandwidth with 128 ports at 800 Gb/s
- Spectrum SN6800: 409.6 Tb/s bandwidth with a remarkable 512 ports at 800 Gb/s

Both platforms are powered by NVIDIA silicon photonics, drastically reducing the number of discrete components and electrical interfaces. The result is a 3.5x leap in power efficiency compared to previous architectures, and a 10x improvement in resiliency by reducing the number of overall optical components that may fail.

## How CPO delivers performance, power, and reliability breakthroughs

- 3.5x power efficiency: By eliminating pluggable transceivers and integrating optics directly into the switch ASIC package, the power required per port drops dramatically, even as network density soars.
- 10x higher resiliency: Fewer discrete active components and the removal of failure-prone transceivers boost uptime and operational reliability.
- 1.3x faster time-to-operation: Streamlined assembly and maintenance translate to accelerated deployment and rapid scaling of AI factories.

With commercial availability for NVIDIA Quantum-X InfiniBand switches set for early 2026 and Spectrum-X Ethernet switches in the second half of 2026, NVIDIA is setting the standard for optimized networking in the age of agentic AI.

Stay tuned for the second part of this blog, where we take a look under the hood of these groundbreaking platforms. From advances in on-chip integration to novel modulation schemes, the next installment will unravel the technologies that set these photonics engines apart.

Source: NVIDIA Technical Blog. URL: https://developer.nvidia.com/blog/scaling-ai-factories-with-co-packaged-optics-for-better-power-efficiency/ . Author Ashkan Seyedi (director of product marketing, ex-Intel/HPE). Published 2025-08-18.
