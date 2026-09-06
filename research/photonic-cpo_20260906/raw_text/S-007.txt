# NVIDIA NVLink: The Scale-Up Network for AI Factories

By Jesse Clayton. NVIDIA Technical Blog. Published 2026-07-20. Modified 2026-08-12.

NVIDIA NVLink is the purpose-built scale-up networking fabric for AI factories, enabling GPUs to work as a single unit of compute with high bandwidth and low latency.

## How scale-up networking determines AI factory economics

Scale-out networks connect servers across the data center. Scale-up networks enable the GPUs inside the domain to behave as a single engine of compute. Both are essential, but they solve different problems.

Scale-out fabrics such as NVIDIA Quantum InfiniBand and NVIDIA Spectrum-X Ethernet enable large clusters spanning thousands to hundreds of thousands of GPUs. Scale-up fabrics connect accelerators in a single domain with high bandwidth, predictable low latency and shared high-bandwidth memory (HBM). For modern AI training and inference, the scale-up domain is where most latency-sensitive communication patterns occur.

## Evaluating scale-up technologies

Spec sheets often compare fabrics using simple bandwidth numbers: link rate, aggregate switch capacity, or headline bandwidth per device. Those numbers are useful, but they aren't sufficient. Evaluating scale-up capabilities for today's AI workloads requires taking a factory-level view. Delivered, full-system performance determines how many tokens can be processed and produced per unit time, power, and factory footprint. It depends on all-to-all fabric bandwidth, end-to-end latency, the in-network compute for reductions and other collectives.

The Key Metrics for Scale-Up Networking in AI Factories: Delivered Performance; Factory Resiliency; Platform Maturity and Proven Supply Chain.

## World-leading performance

With Vera Rubin NVL72, sixth generation NVLink provides 3.6 TB/s per GPU of bidirectional GPU-to-GPU bandwidth and 260 TB/s of rack-level GPU bandwidth in a 72-GPU domain. The end-to-end latency for GPU-to-GPU transfers is 3X lower than alternative solutions based on off-the-shelf Ethernet, and the packet rate is 10X higher.

NVLink Switch trays and NVLink spine of 5,000 cables form a single all-to-all topology so any GPU can communicate with any other GPU with uniform latency and bandwidth. Each tray includes four NVLink 6 switch chips, 28.8 TB/s of total tray bandwidth, and 14.4 TFLOPS of FP8 in-network compute. In a single Vera Rubin NVL72 rack, NVLink 6 provides 260 TB/s of aggregate bandwidth and 130 TFLOPS of in-network compute.

The NVLink technology roadmap includes support for scale-up domain sizes up to 1152 GPUs and connectivity through co-packaged optics.

## Mature technology on a fast cadence

NVLink is now in its sixth generation of purpose-built scale-up networking fabric. It has been production-deployed at scale for nearly a decade, with millions of NVIDIA chips deployed across NVLink-capable systems and an ecosystem of servers, racks, cables, switches, software, and operations tooling.

## NVLink-C2C extends the fabric to CPUs

With Vera CPUs in the Vera Rubin NVL72 platform, NVLink-C2C delivers 1.8 TB/s of coherent bandwidth between CPUs and GPUs, 7x the bandwidth of PCIe Gen6.

Source: NVIDIA Technical Blog. URL: https://developer.nvidia.com/blog/nvidia-nvlink-the-scale-up-network-for-ai-factories/ . Author Jesse Clayton (principal product marketing manager, AI infrastructure). Published 2026-07-20.
