# -*- coding: utf-8 -*-
"""Single source of truth for sangmin2-rf.github.io.
Edit this file, then run:  python build.py   -> regenerates docs/
"""

SITE_URL = "https://sangmin2-rf.github.io"
UPDATED = "Nov. 2026"

PROFILE = {
    "name": "Sangmin Lee",
    "name_ko": "이상민",
    "title": "Ph.D. Student",
    "dept": "School of Electronic and Electrical Engineering",
    "univ": "Kyungpook National University",
    "lab": "PLAYWAVE Lab",
    "lab_url": "https://playwave.knu.ac.kr/",
    "location": "Daegu, Republic of Korea",
    "office": "IT-1 Bldg. Room 905, 80 Daehak-ro, Buk-gu, Daegu 41566, Korea",
    "email_user": "sangmin2", "email_domain": "knu.ac.kr",
    "photo": "assets/prof_pic.jpg",
    "links": [
        ("ORCID", "https://orcid.org/0000-0003-4959-6215"),
        ("IEEE Xplore", "https://ieeexplore.ieee.org/author/37089670646"),
        ("GitHub", "https://github.com/sangmin2-rf"),
        ("Lab Homepage", "https://playwave.knu.ac.kr/"),
    ],
}

ABOUT = [
    "I am a Ph.D. student in the School of Electronic and Electrical Engineering at Kyungpook National University (KNU), "
    "advised by <a href='https://research.knu.ac.kr/en/persons/sangjo-choi/'>Prof. Sangjo Choi</a> in the "
    "<a href='https://playwave.knu.ac.kr/'>PLAYWAVE Lab</a>. I received the B.S. degree from the University of Ulsan in 2021 "
    "and the M.S. degree from KNU in 2024.",
    "My research focuses on controlling electromagnetic waves with metasurfaces and antenna arrays &mdash; from unit-cell design "
    "and full-wave simulation to PCB prototyping, anechoic-chamber pattern measurement, and over-the-air link validation.",
    "My doctoral research on a Moir&eacute;-based transparent transmissive RIS for 6G outdoor-to-indoor links is supported by the "
    "NRF Ph.D. Student Research Grant (RS-2026-25552947).",
]

INTERESTS = [
    ("Reconfigurable Intelligent Surfaces for 6G Upper Mid-Band", "RIS"),
    ("Millimeter-Wave Series-Fed Arrays for Automotive Radar", "mmWave"),
    ("Metasurface-Enabled Electromagnetic Computing and Imaging", "EM Computing"),
    ("Beam-Steering Phased Arrays for SATCOM", "SATCOM"),
]

# kind: paper | award | grant | talk | milestone
NEWS = [
    ("2026-11-02", "paper", "Co-authored paper with Subin Lee accepted in <b>IEEE Transactions on Antennas and Propagation</b> (beamforming series-feed patch array)."),
    ("2026-09-14", "award", "Co-authored paper with Kihan Park received the <b>Best Paper Award</b> at the 2026 KIEES Summer Conference."),
    ("2026-09-01", "grant", "Started the <b>NRF Ph.D. Student Research Grant</b> project (RS-2026-25552947) as PI: <i>Moir&eacute;-Based Transparent Transmissive RIS for 6G Outdoor-to-Indoor Links</i>."),
    ("2026-07-13", "talk", "Presented <b>Dynamic Huygens' STAR-RIS</b> at the 2026 IEEE AP-S/URSI, Detroit, MI, USA."),
    ("2026-03-19", "award", "Three awards as co-author at the 2026 KIEES Winter Conference: two <b>Best Paper Awards</b> and the <b>6th Student Project Exhibition &amp; Competition</b> award."),
    ("2026-02-01", "paper", "Co-authored paper published in <b>IEEE Open Journal of Antennas and Propagation</b>."),
    ("2025-08-20", "talk", "Presented transmissive-RIS-based outdoor-to-indoor 5G NR link enhancement at the 2025 KIEES Summer Conference."),
    ("2025-08-01", "paper", "First-author paper published in <b>JKIEES</b> (path-loss modeling of transmissive RIS)."),
    ("2025-07-02", "award", "Received the <b>DB HiTek Scholarship</b> at the KNU-EE Research Congress 2025."),
    ("2025-03-22", "paper", "First-author paper published in <b>Advanced Materials Technologies</b>."),
    ("2025-02-12", "talk", "Presented a transmissive RIS repeater for Wi-Fi 6 1024-QAM signals at the 2025 KIEES Winter Conference."),
    ("2025-02-01", "paper", "Co-authored paper published in <b>IEEE Transactions on Antennas and Propagation</b>."),
    ("2024-11-08", "talk", "Presented an electrically tunable planar Huygens' metasurface at <b>ISAP 2024</b>, Incheon, Korea."),
    ("2024-08-21", "talk", "Presented a reconfigurable planar Huygens' metasurface with &plusmn;70&deg; beam scanning at the 2024 KIEES Summer Conference."),
    ("2024-07-02", "award", "Received the <b>Best Paper Award</b> at the KNU-EE Research Congress 2024."),
    ("2024-03-01", "milestone", "Started the Ph.D. program at Kyungpook National University."),
    ("2024-02-05", "milestone", "Korean patent on microstrip traveling-wave series-fed array antennas registered (KR 10-2633315)."),
]

EDUCATION = [
    {"period": "2024.03 — Present", "degree": "Ph.D. in Electronic and Electrical Engineering",
     "school": "Kyungpook National University (KNU)", "url": "https://www.knu.ac.kr/", "place": "Daegu, Republic of Korea",
     "advisor": ("Sangjo Choi", "https://research.knu.ac.kr/en/persons/sangjo-choi/"), "logo": "assets/logos/knu.jpg"},
    {"period": "2022.03 — 2024.02", "degree": "M.S. in Electronic and Electrical Engineering",
     "school": "Kyungpook National University (KNU)", "url": "https://www.knu.ac.kr/", "place": "Daegu, Republic of Korea",
     "advisor": ("Sangjo Choi", "https://research.knu.ac.kr/en/persons/sangjo-choi/"), "logo": "assets/logos/knu.jpg"},
    {"period": "2014.03 — 2021.08", "degree": "B.S. in Electrical, Electronics and Computer Engineering",
     "school": "University of Ulsan", "url": "https://www.ulsan.ac.kr/", "place": "Ulsan, Republic of Korea",
     "advisor": None, "logo": "assets/logos/ulsan.png"},
]

# ---------------------------------------------------------------- publications
ME = ["S. Lee", "Sangmin Lee", "S.-M. Lee", "Sang-Min Lee"]

JOURNALS = [
    {"key": "lee2026beamforming", "selected": True, "first": False, "jabbr": "IEEE TAP",
     "authors": "Subin Lee, **S. Lee**, D. Lee, and S. Choi*",
     "title": "Beamforming Series-Feed Patch Antenna Array for Wideband Uniform and Chebyshev Power Distributions",
     "venue": "IEEE Transactions on Antennas and Propagation (TAP), Communication — accepted Nov. 2026, to appear",
     "doi": None, "year": 2026, "status": "Accepted",
     "keywords": ["Series array antenna", "Series feed network", "Power distribution"],
     "abstract": "This paper addresses, for the first time, the issue of the power distribution degradation in beamforming series-feed networks resulting from out-of-band deviations in the input impedance of the phase shifter. To resolve this issue, the optimum length of the transmission-line section between junctions in the series-feed network is determined. A continuous 360° reflection-type phase shifter (RTPS) with 1-bit switching, whose insertion loss and input impedance exhibit only small variations across its states as the design rule requires, is adopted. As a proof of concept, 4 × 1 beamforming series-feed patch antenna arrays employing the proposed feed network and phase shifter are designed at 5.5 GHz for the uniform and Chebyshev distributions. Both fabricated arrays exhibit sidelobe levels below −13 dB over a 470-MHz power-distribution bandwidth, with a 1-dB gain bandwidth at broadside of 180 MHz for both the uniform and Chebyshev distributions, a peak gain of ∼8 dBi, and a beam steering range of −45° to +45°. The design rule is further verified on a simulated eight-element array, which keeps the SLL below −16.5 dB over 5.2–5.8 GHz."},
    {"key": "kim2026synthesis", "selected": True, "first": False, "jabbr": "IEEE OJAP",
     "authors": "T. Kim, F. Zardi, S. Lee, J. Kim, U. Park, J. Oh, S. Choi*, and G. Oliveri",
     "title": "On the Synthesis of Aperiodic Multi-Atom 1-Bit Reconfigurable Passive EMSs at 140 GHz",
     "venue": "IEEE Open Journal of Antennas and Propagation (OJAP), vol. 7, no. 1, pp. 265–276, Feb. 2026",
     "doi": "10.1109/OJAP.2025.3643633", "year": 2026,
     "keywords": ["Electromagnetic skins (EMSs)", "Reconfigurable intelligent surfaces (RIS)", "Smart EM environment (SEME)", "Multi-atom skin", "Surface electromagnetics", "Next-generation communications"],
     "abstract": "An innovative reconfigurable passive electromagnetic skin (RP-EMS) architecture is proposed to support a single reflection beam while suppressing undesired beams, using 1-bit switching with minimal hardware complexity. The architecture is the first to simultaneously optimize the meta-atom arrangement and their 1-bit switching descriptors using the integer-coded evolutionary algorithm, supporting multiple reflection scenarios. The process yields one aperiodic meta-atom arrangement that effectively mitigates periodic phase quantization errors typical of 1-bit RP-EMS layouts, while changing reflection angles solely through 1-bit switching. An aperture-coupled patch-based meta-atom topology with well-separated and linearized phase responses is employed to enable 1-bit switching using a short/open connection. As a proof of concept, 30×30 RP-EMS prototypes with a 3.14×3.14 cm² aperture and λ/2 periodicity at 140 GHz are designed and fabricated, demonstrating reflection at 15°, 30°, and 45° under normal incidence. The prototypes exhibited robust beam steering with QLL consistently below −10 dB and SLL up to −10 dB, confirming the effectiveness of the proposed MASB layout. In addition, the structures achieve 3-dB gain bandwidth exceeding 11% and high reflection efficiencies over 15%, referenced to a conductor surface of the same size. These results validate the potential of the proposed architecture for implementing multi-functional 1-bit RP-EMS with controlled sidelobes and no grating lobe near 140 GHz."},
    {"key": "lee2025pathloss", "selected": False, "first": True, "jabbr": "JKIEES",
     "authors": "S. Lee and S. Choi*",
     "title": "Path Loss Modeling and Communication Performance Verification of Transmissive RIS in Simulated Outdoor-to-Indoor Channels",
     "venue": "The Journal of Korean Institute of Electromagnetic Engineering and Science (JKIEES), vol. 36, no. 8, pp. 737–748, Aug. 2025",
     "doi": "10.5515/KJKIEES.2025.36.8.737", "year": 2025,
     "keywords": ["Transmissive RIS", "Outdoor-to-indoor communication", "Repeater system", "Path loss model", "Wi-Fi 6"],
     "abstract": "Transmissive reconfigurable intelligent surfaces (TRIS) have emerged recently as promising relay technologies for 6G communication, mitigating the signal attenuation caused by outdoor-to-indoor (O2I) propagation loss. Typically installed at the O2I boundary, TRIS can enhance the connectivity between outdoor base stations and indoor devices. This study experimentally investigates a TRIS-based relay system for O2I communication using IEEE 802.11ax (Wi-Fi 6) signals at 5.5 GHz. Experimental results demonstrate an improvement of up to 19.5 dB in the received signal power compared to scenarios without the TRIS. This improvement surpasses path loss model predictions by 11.8 dB due to multipath effects. Additionally, the measured error vector magnitude (EVM) met Wi-Fi 6 standards (below −30 dB at MCS 8). These findings validate TRIS as effective solutions for addressing shadowed areas and improving the signal quality in O2I environments at 5.5 GHz."},
    {"key": "lee2025reconfigurable", "selected": True, "first": True, "jabbr": "Adv. Mater. Technol.",
     "authors": "S. Lee and S. Choi*",
     "title": "Reconfigurable Planar Huygens' Metasurface for Wide Beamforming",
     "venue": "Advanced Materials Technologies, vol. 10, no. 13, Art. no. 2402131, 2025",
     "doi": "10.1002/admt.202402131", "year": 2025,
     "keywords": ["Beamforming", "Huygens' metasurface", "Reconfigurable intelligent surface"],
     "abstract": "Huygens' metasurfaces (HMSs), which independently control electric and magnetic dipole responses, have been implemented in planar platforms. However, dynamically controlling both dipole responses to achieve reconfigurability at the sub-wavelength scale remains challenging with conventional planar HMSs. In this work, these challenges are addressed by introducing the first planar, reconfigurable HMS design that integrates varactors and embedded bias lines, allowing for precise and independent control of electric and magnetic surface impedances at the sub-wavelength scale (λ0/9.4 × λ0/6.3 × λ0/22.7) at 5.5 GHz. A large-aperture HMS (4.47λ0 × 4.47λ0), integrated with 3,528 varactors and fed by a 4 × 4 patch array at a focal-length-to-diameter ratio of 1.6, demonstrates wide beamforming angles ranging from −70° to +70° with an aperture efficiency of 21.09%. This innovative design offers a promising solution for efficient and compact reconfigurable intelligent surfaces, paving the way for advanced wave control in next-generation wireless communication and sensing applications."},
    {"key": "kim2025prephased", "selected": True, "first": False, "jabbr": "IEEE TAP",
     "authors": "T. Kim, S. Lee, S. Oh, J. Kim, J. Oh, and S. Choi*",
     "title": "Pre-Phased 1-bit Reflective Passive Metasurface With Optimum Number of Pre-Phasing for Low QLL and SLL at 140 GHz",
     "venue": "IEEE Transactions on Antennas and Propagation (TAP), vol. 73, no. 2, pp. 975–985, Feb. 2025",
     "doi": "10.1109/TAP.2024.3510861", "year": 2025,
     "keywords": ["Pre-phased 1-bit metasurface (MS)", "Quantization lobe (QL)", "Reconfigurable intelligent surface (RIS)", "Reflective metasurface"],
     "abstract": "Recent advancements introduced a pre-phased reflective metasurface (MS) using 1-bit control to suppress the quantization lobe (QL) inherent in a typical 1-bit MS under plane wave incidence, particularly in millimeter and submillimeter wave bands. However, the optimal method for pre-phasing using random phases has yet to be fully explored. This study investigates the optimal number of pre-phasing, which denotes the minimum number of discrete random phases for effective suppression of QLs and side lobes while ensuring low design complexity. The results indicate that employing four discrete phases, equally spaced at 45° intervals, is the optimal solution for both normal and oblique incidences. The random phases with a 45° separation are implemented into four pairs of unit cells with passive on/off switching using multilayer PCBs at 140 GHz. Each unit cell consisted of a metallic patch coupled to a transmission (Tx) line through a slot, with embedded static on/off switching in the Tx line to enable 1-bit reflection phase control. Finally, three MSs with 30×30 unit cells, each with fixed random pre-phases, are designed and fabricated to reflect normal incidence at reflection angles (θr) of 15°, 30°, and 45° at 140 GHz. The experiment results demonstrate peak reflected beams at 15°, 29°, and 45° with frequencies of 139.7, 139.1, and 135.9 GHz, respectively. In addition, significant reductions in QL to −20 dB were observed, along with a reflection efficiency of 26%, and a 3 dB gain bandwidth exceeding 10%, on average, across all reflection angles in the 140 GHz band."},
    {"key": "lee2023universal", "selected": True, "first": True, "jabbr": "IEEE TAP",
     "authors": "S. Lee and S. Choi*",
     "title": "Universal and Non-Iterative Design Method for In-Phase Radiation of Microstrip Traveling-Wave Series-Fed Antenna Arrays",
     "venue": "IEEE Transactions on Antennas and Propagation (TAP), vol. 71, no. 2, pp. 1403–1413, Feb. 2023",
     "doi": "10.1109/TAP.2022.3227751", "year": 2023,
     "keywords": ["Comb-line array", "Millimeter-wave antenna array", "Series-fed patch array", "Traveling-wave series-fed antenna array"],
     "abstract": "Microstrip traveling-wave series-fed antenna arrays (MTSAAs) have been popularly developed for radar systems in the millimeter-waveband. Because the antennas are connected and fed in series in MTSAA, in-phase radiation of the antenna elements with properly tapered amplitude for achieving a broadside beam with a low sidelobe level (SLL) is challenging. Although the reported series-fed patch and comb-line arrays accomplished the goal, design equations for the optimum distances between antenna elements in the series-fed array do not guarantee in-phase radiation due to the mutual coupling in array structures. Therefore, optimization of the distances in the array using full-wave simulations is inevitable. In this article, we propose the first universal and non-iterative design equation that compensates for the phase offset generated in patch and comb-line MTSAAs and successfully found optimum distances for broadside beams with low SLLs without optimization. Finally, we fabricated both MTSAAs with ten elements operating at 76.5 GHz and demonstrated almost 13 dB boresight gain and low SLLs near −18 dB without a beam tilt."},
    {"key": "lee2021dbd", "selected": False, "first": True, "jabbr": "ASCT",
     "authors": "S.-M. Lee and J. Choi*",
     "title": "Intensity and Uniformity Enhancement of Dielectric Barrier Discharge by Using Silver-Coated Electrode",
     "venue": "Applied Science and Convergence Technology (ASCT), vol. 30, no. 1, pp. 29–33, Jan. 2021",
     "doi": "10.5757/ASCT.2021.30.1.29", "year": 2021,
     "keywords": ["Dielectric barrier discharge", "Image processing", "Intensity", "Silver mirror reaction", "Uniformity"],
     "abstract": "The intensity and uniformity of the dielectric barrier discharge (DBD) were studied via fabrication. The DBD can be achieved by various methods using dielectrics and electrodes; however, depending on the device configuration and fabrication method, unnecessary air gaps may occur between the dielectric and electrode. The air gap increases the breakdown voltage for plasma generation, thereby affecting the characteristics of the DBD. In this study, an inner electrode was formed on the surface of a dielectric by the silver mirror reaction to eliminate the air gap; in this technique, silver is deposited on the dielectric surface by a reducing organic compound. The DBD images of the silver-coated inner electrode were investigated using an intensified charge coupled device (ICCD) camera and the OpenCV library of Python for quantitatively evaluating performance measures such as intensity and uniformity. In addition, the reactive oxygen species (ROS) generated by DBD were measured with a band-pass filter and the ICCD camera. When the DBD device was driven by same voltages, the silver-coated inner electrode showed improved intensities and uniformities of up to 7.98 and 1.75 times, respectively. Moreover, the ROS intensities and uniformities were improved by up to 57.8 and 9.27 times, respectively."},
]

JOURNAL_FULL = {
    "IEEE TAP": "IEEE Transactions on Antennas and Propagation",
    "IEEE OJAP": "IEEE Open Journal of Antennas and Propagation",
    "Adv. Mater. Technol.": "Advanced Materials Technologies (Wiley)",
    "JKIEES": "The Journal of Korean Institute of Electromagnetic Engineering and Science",
    "ASCT": "Applied Science and Convergence Technology",
}

INTL_CONF = [
    {"key": "lee2026aps", "authors": "S. Lee and S. Choi",
     "title": "Dynamic Huygens' STAR-RIS: Simultaneous Transmitting and Reflecting Reconfigurable Intelligent Surface",
     "venue": "2026 IEEE International Symposium on Antennas and Propagation and USNC-URSI Radio Science Meeting (AP-S/URSI 2026)",
     "place": "Detroit, MI, USA, Jul. 12–17, 2026", "year": 2026, "doi": None,
     "keywords": ["STAR-RIS", "Huygens' metasurface", "Reconfigurable intelligent surface", "Full-space beam steering"],
     "abstract": "This work reports an experimental demonstration of a fully electronically controllable simultaneously transmitting and reflecting reconfigurable intelligent surface (STAR-RIS) based on Huygens' principle at 5.4 GHz. Inspired by Huygens' metasurface, the proposed RIS realizes independent control of electric and magnetic surface impedances using varactor-embedded electric and magnetic dipoles implemented in a two-layer PCB, each driven by dedicated bias networks. A prototype with a 4.39λ0 × 4.39λ0 aperture at 5.4 GHz achieved phase tunability of 160° in transmission and 260° in reflection, with average |S21| and |S11| of −5.75 dB and −4.86 dB at 5.4 GHz, respectively. Dynamic STAR functionality is experimentally validated by feeding the RIS with a patch array while rotating the prototype 360°, enabling simultaneous characterization of both transmission and reflection responses. The STAR-RIS demonstrates beam steering up to 45° in both modes, with maximum gains of 16.1 dBi (transmission) and 14.8 dBi (reflection). By enabling bidirectional and independently reconfigurable wavefront control, the demonstrated STAR-RIS offers a practical route toward extending wireless coverage across outdoor-indoor interfaces through concurrent forward and backward link enhancement."},
    {"key": "lee2024isap", "authors": "S. Lee and S. Choi",
     "title": "Electrically Tunable Planar Huygens' Metasurface for Wide Beam Coverage",
     "venue": "2024 International Symposium on Antennas and Propagation (ISAP 2024)",
     "place": "Incheon, Republic of Korea, Nov. 2024", "year": 2024, "doi": None,
     "keywords": ["Reconfigurable Huygens' metasurface", "Beam steering", "Transmitarray"],
     "abstract": "This study introduces a novel electrically tunable planar Huygens' metasurface (HMS) for wide beam coverage. The HMS unit cell, constructed on a two-layer planar FR4 substrate with subwavelength dimensions at 5.5 GHz, integrates both electric and magnetic dipoles compactly. The HMS unit cell achieves electrical tunability by incorporating varactors within the dipoles, allowing for independent control of the electric and magnetic surface impedances. To validate the beam steering capability, a large-scale HMS was fabricated and verified, fed through a 4 × 4 patch array antenna located at an F/D ratio of 1.6. Measurement results at 5.4 GHz confirmed a wide transmission phase coverage, a maximum gain of 10.96 dB, and a beam steering range from −70° to +70°."},
    {"key": "lee2022isap", "authors": "S. Lee and S. Choi",
     "title": "Universal Design Method for Traveling Wave Series-Fed Array Antennas",
     "venue": "2022 International Symposium on Antennas and Propagation (ISAP 2022), pp. 99–100",
     "place": "Sydney, Australia, Oct. 2022", "year": 2022, "doi": "10.1109/ISAP53582.2022.9998856",
     "keywords": ["Traveling-wave series-fed antenna array", "Comb-line array", "Series-fed patch array"],
     "abstract": "Microstrip traveling-wave series-fed array antennas are popularly utilized for millimeter-wave radars and communication systems due to low loss from a feeding network. However, the design difficulty compared to parallel-fed arrays for in-phase radiation is inevitable due to the loading and mutual coupling effects between the antenna elements connected in one single feeding line. For the in-phase radiation, the distances between antenna units have been tuned, but the tuning process is cumbersome due to the interdependence between the units. This paper introduces a universal and tuning-free design method of microstrip traveling-wave series-fed arrays for in-phase radiation. We designed series-fed patch and comb-line arrays operating at 76.5 GHz based on the proposed method and proved the in-phase radiation with the main beam at the boresight and a sidelobe level near -20dB."},
    {"key": "lee2022aps", "authors": "S. Lee and S. Choi",
     "title": "Active Double-Layered Huygens' Metasurface for Beamforming Application",
     "venue": "2022 IEEE International Symposium on Antennas and Propagation and USNC-URSI Radio Science Meeting (AP-S/URSI 2022)",
     "place": "Denver, CO, USA, Jul. 2022", "year": 2022, "doi": None, "keywords": [], "abstract": ""},
    {"key": "islam2021isap", "authors": "K. M. R. Islam, S. Lee, and S. Choi",
     "title": "Tunable Huygens' Transmission Metasurface on Double-Layer PCB",
     "venue": "2021 International Symposium on Antennas and Propagation (ISAP 2021)",
     "place": "Taipei, Taiwan, Oct. 2021", "year": 2021, "doi": None, "keywords": [], "abstract": ""},
]

# (year, month, authors, title, conference, note, award)
DOMESTIC = [
    (2026, "Aug.", "K. Park, S. Lee, and S. Choi", "X-circuit 등가회로를 이용한 호이겐스 메타표면 임피던스 공진 정합 조건에 따른 특성 분석", "2026 KIEES Summer Conf.", "", "Best Paper Award"),
    (2026, "Aug.", "S. Kwon, S. Lee, and S. Choi", "Accurate Diode Equivalent Circuit Extraction via TRL Calibration with DUT Pad De-embedding", "2026 KIEES Summer Conf.", "", ""),
    (2026, "Aug.", "C. Choi, S. Lee, B. Kim, J. Oh, and S. Choi", "250 GHz 대역 PCB 기반 투과형 배열 안테나의 최대 이득을 위한 최적화 설계", "2026 KIEES Summer Conf.", "", ""),
    (2026, "Feb.", "S. Lee and S. Choi", "Transmissive Reconfigurable Intelligent Surface Based on Huygens' Principle for 6G Upper-Mid Band Outdoor-to-Indoor Coverage Enhancement", "2026 KIEES Winter Conf.", "", ""),
    (2026, "Feb.", "H. Shin, S. Lee, and S. Choi", "홀로그래픽 안테나 개구 효율 개선을 위한 Tensor Unit Cell 설계", "2026 KIEES Winter Conf.", "", "Best Paper Award"),
    (2026, "Feb.", "S. Kwon, Subin Lee, **S. Lee**, and S. Choi", "Sub-6 GHz Band Diode's Equivalent Circuit Extraction using TRL Calibration", "2026 KIEES Winter Conf.", "", "Best Paper Award"),
    (2026, "Feb.", "K. Park, S. Lee, and S. Choi", "인터디지털 기생 스트립을 포함한 I-형 공진기 유닛셀의 표면 임피던스 변화 분석", "2026 KIEES Winter Conf.", "", ""),
    (2026, "Feb.", "C. Choi, S. Lee, and S. Choi", "250 GHz 대역 다채널 안테나 이득 향상을 위한 이중 편파 투과형 배열 안테나 설계", "2026 KIEES Winter Conf. (6th Student Project Exhibition)", "", "Student Project Award"),
    (2025, "Aug.", "S. Lee and S. Choi", "투과형 RIS 기반 실외-실내 5G NR 링크의 커버리지 개선 및 성능 검증", "2025 KICSF Summer Conf.", "", ""),
    (2025, "Aug.", "S. Lee and S. Choi", "실외-실내 통신 중계를 위한 투과형 RIS 기반 링크 성능 향상 검증", "2025 KIEES Summer Conf.", "", ""),
    (2025, "Aug.", "H. Shin, S. Lee, and S. Choi", "홀로그래픽 안테나의 Aperture Field 기반 모델링 및 중심 급전으로 인한 주빔 Null 현상 분석", "2025 KIEES Summer Conf.", "", ""),
    (2025, "Feb.", "S. Lee, C. Kim, and S. Choi", "Experimental Validation of Transmissive RIS as a Repeater for Wi-Fi 6 1024-QAM Signals", "2025 KIEES Winter Conf.", "", ""),
    (2024, "Aug.", "S. Lee and S. Choi", "Reconfigurable Intelligent Surface Using Huygens' Principle for Wide Beam Scanning", "2024 KIEES Summer Conf.", "", ""),
    (2023, "Aug.", "S. Lee and S. Choi", "Experimental Verification of Active Beam Steering Performance of Digitally-Controlled Huygens' Metasurface", "2023 KIEES Summer Conf.", "Oral", ""),
    (2023, "Feb.", "S. Lee and S. Choi", "Investigation on Optimal Focal Distance between Feeding Antenna and Huygens' Metasurface", "2023 KIEES Winter Conf.", "Oral", ""),
    (2022, "Aug.", "S. Lee and S. Choi", "Design and Implementation of Active Transmissive Double-Layer Huygens' Metasurface for Beamforming Application", "2022 KIEES Summer Conf.", "Oral", "IEEE AP-S Seoul Chapter Chair Award"),
    (2022, "Feb.", "S. Lee and S. Choi", "Varactor-Tuned Beam-Forming Huygens' Metasurface", "2022 KIEES Winter Conf.", "Oral", ""),
    (2021, "Aug.", "S. Lee and S. Choi", "Design of Traveling-Wave Microstrip Antenna Arrays with Low-Sidelobe Level and In-Phase Excitation", "2021 KIEES Summer Conf.", "Poster", "Best Paper Award (Undergraduate)"),
    (2021, "Aug.", "K. M. R. Islam, S. Lee, T. Kim, and S. Choi", "Reconfigurable Transmission Huygens' Metasurface on Compact Double-Layered PCB for Beamforming Application", "2021 KIEES Summer Conf.", "Oral", ""),
    (2021, "Feb.", "S. Lee and S. Choi", "Optimization Method for Low SLL Millimeter-Wave Microstrip Comb-Line Antenna Array", "2021 KIEES Winter Conf.", "Poster", "Best Paper Award (Undergraduate)"),
    (2020, "Nov.", "S. Lee, S. Choi, and J. Choi", "Study on Electrode Fabrication to Enhance DBD Intensity and Uniformity", "2020 KIEES Autumn Conf.", "Poster", ""),
    (2020, "Aug.", "S. Lee and S. Choi", "Millimeter-Wave Microstrip Comb-Line Antenna Array Using Stub-Integrated Rounded Radiating Element", "2020 KIEES Summer Conf.", "Poster", ""),
    (2020, "Aug.", "S. Lee, J. Lee, S. Kim, and S. Choi", "Water Pump Monitoring System", "2020 KIEES Summer Conf.", "Poster", ""),
    (2020, "Aug.", "S. Lee, J. Kim, J. Lee, S. Kim, J. Choi, and S. Choi", "Plasma Activated Water for Sterilization by Dielectric Barrier Discharge", "2020 KIEES Summer Conf.", "Poster", ""),
]

PATENTS = [
    {"title": "Microstrip Traveling-Wave Series-Fed Array Antennas and Design Method Thereof",
     "inventors": "S. Choi and S. Lee", "country": "Korea", "status": "Registered",
     "number": "10-2633315", "date": "2024.02.05", "filed": "2022.06.14",
     "url": "https://patents.google.com/patent/KR102633315B1/en"},
    {"title": "Active Huygens' Metasurface Unit Cell and Huygens' Metasurface Array Including the Same (능동형 호이겐스 메타표면 유닛셀 및 이를 포함하는 호이겐스 메타표면 배열)",
     "inventors": "S. Choi and S. Lee", "country": "Korea", "status": "Filed",
     "number": "10-2022-0135748", "date": "2022.10.20", "filed": "2022.10.20", "url": None},
]

# ---------------------------------------------------------------- awards
AWARDS = [
    ("Research Grants & Scholarships", [
        ("NRF Ph.D. Student Research Grant", "Principal Investigator · No. RS-2026-25552947", "National Research Foundation of Korea", "Sep. 2026 –", True),
        ("DB HiTek Scholarship", "", "KNU-EE Research Congress 2025", "Jul. 2025", True),
        ("Corporate Scholarship", "", "Hanju Corporation", "2019", False),
        ("Academic Scholarship", "", "University of Ulsan", "2018 – 2020", False),
    ]),
    ("Conference Awards (Domestic)", [
        ("Best Paper Award", "Co-author (with K. Park)", "2026 KIEES Summer Conference", "Aug. 2026", False),
        ("Best Paper Award", "Co-author (with H. Shin)", "2026 KIEES Winter Conference", "Feb. 2026", False),
        ("Best Paper Award", "Co-author (with S. Kwon and S. Lee)", "2026 KIEES Winter Conference", "Feb. 2026", False),
        ("6th Student Project Exhibition & Competition Award", "Co-author (with C. Choi)", "2026 KIEES Winter Conference", "Feb. 2026", False),
        ("IEEE AP-S Seoul Chapter Chair Award", "", "2022 KIEES Summer Conference", "Aug. 2022", True),
        ("Best Paper Award (Undergraduate Student Paper)", "", "2021 KIEES Summer Conference", "Aug. 2021", True),
        ("Best Paper Award (Undergraduate Student Paper)", "", "2021 KIEES Winter Conference", "Feb. 2021", True),
        ("Best Paper Award (Undergraduate Student Paper)", "", "2020 KIEES Summer Conference", "Aug. 2020", True),
        ("Best Paper Award (Creative Competition)", "", "2020 KIEES Summer Conference", "Aug. 2020", True),
    ]),
    ("Institutional Research Awards", [
        ("Best Paper Award", "", "KNU-EE Research Congress 2024", "Jul. 2024", True),
        ("Best Paper Award", "", "KNU-EE Research Congress 2022", "2022", True),
    ]),
    ("Undergraduate Competitions", [
        ("Third Prize", "", "2020 University of Ulsan Research Intern", "2020", False),
        ("Second Prize", "", "2020-1 University of Ulsan Capstone Contest", "2020", False),
        ("First Prize", "", "2019-2 University of Ulsan Capstone Contest", "2019", False),
        ("First Prize", "", "Smart Factory Convertible ICT Maker-Tone", "2019", False),
        ("Achievement Award", "", "Building Smart Factory with Naval Logistics Command and University of Ulsan", "2019", False),
        ("Participation Award", "", "2019 Regional Strategy Industry Hackathon", "2019", False),
    ]),
]

# ---------------------------------------------------------------- research projects
PROJECTS = [
    {"period": "2026.09 — 2028.08 (planned)", "title": "Moiré-Based Transparent Transmissive Reconfigurable Intelligent Surface for 6G Outdoor-to-Indoor Links",
     "org": "National Research Foundation of Korea (NRF) · Ph.D. Student Research Grant", "no": "RS-2026-25552947", "role": "Principal Investigator",
     "bullets": ["Metal-mesh-based optically transparent Huygens' metasurface unit cell for the 6G upper mid-band (FR3).",
                 "Mechanical beam steering with a Moiré lens pair driven by linear displacement; HW/SW co-optimization of the motorized prototype.",
                 "Over-the-air O2I link validation (EVM, throughput) with commercial 6G test equipment."]},
    {"period": "Since 2024", "title": "Development of RIS and NCR Component Technologies for Upper-mid Band Smart Repeater",
     "org": "Institute of Information & Communications Technology Planning & Evaluation (IITP)", "no": "RS-2024-00395366", "role": "Participating Researcher",
     "bullets": ["Transmissive RIS as an outdoor-to-indoor repeater: Wi-Fi 6 (1024-QAM) and 5G NR link-enhancement measurements.",
                 "STAR-RIS (simultaneous transmitting and reflecting) prototype based on Huygens' metasurface."]},
    {"period": "Since 2021", "title": "Innovative Fusion Technologies of Intelligent Antenna Material/Structure/Network for THz 6G",
     "org": "Institute of Information & Communications Technology Planning & Evaluation (IITP)", "no": "2021-0-00763", "role": "Participating Researcher",
     "bullets": ["Reconfigurable planar Huygens' metasurface with 3,528 varactors and ±70° beam steering at 5.4 GHz.",
                 "250 GHz PCB-based transmitarray antenna design (with Seoul National University)."]},
]

# ---------------------------------------------------------------- service / mentoring / coursework
SERVICE = [
    ("Conference Reviewer", ["IEEE AP-S/URSI 2027 (paper review invitation)"]),
]

MENTORING = [
    ("Mentored students (co-authored work)", [
        "Seongun Kwon (M.S. student) — diode equivalent-circuit extraction via TRL calibration; 2026 KIEES Winter Best Paper Award",
        "Hyowon Shin (B.S. student) — holographic antenna modeling and tensor-impedance unit cells; 2026 KIEES Winter Best Paper Award",
        "Kihan Park (B.S. student) — Huygens' metasurface impedance matching analysis; 2026 KIEES Summer Best Paper Award",
        "Chanyoung Choi (B.S. student) — 250 GHz PCB transmitarray; 2026 KIEES Winter Student Project Award",
    ]),
    ("Collaborators", [
        "Prof. Jungsuek Oh — Seoul National University (140 GHz metasurfaces, 250 GHz transmitarray)",
        "Prof. Giacomo Oliveri &amp; Dr. Francesco Zardi — ELEDIA Research Center, University of Trento, Italy (aperiodic 1-bit EMSs)",
    ]),
]

SKILLS = [
    ("EM Simulation", "Ansys HFSS, AWR Microwave Office"),
    ("PCB & Mechanical", "Altium Designer, AutoCAD, Fusion 360"),
    ("Measurement", "VNA, anechoic-chamber radiation pattern, OTA link test (EVM, throughput)"),
    ("Programming", "MATLAB, Python"),
]
