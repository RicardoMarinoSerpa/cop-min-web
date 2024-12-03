import streamlit as st
from datetime import datetime, date
import requests

# Configuración de la página
st.set_page_config(
    page_title="Mining Event Classification",
    page_icon="⛏️",
    layout="centered"
)

# Estilos personalizados
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: #e0e0e0;
        font-family: Arial, sans-serif;
    }
    .title {
        text-align: center;
        font-size: 36px;
        color: #76ff03;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .description {
        text-align: center;
        font-size: 18px;
        color: #bdbdbd;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 18px;
        font-weight: bold;
        margin-top: 20px; /* Espacio superior entre secciones */
        margin-bottom: 5px; /* Espacio entre el título y la descripción */
    }
    .section-description {
        font-size: 12px;
        margin-top: 0; /* Sin espacio superior */
        margin-bottom: -40px; /* Espacio entre la descripción y el selectbox */
    }
    .section-header {
        font-size: 24px;
        color: #76ff03;
        border-bottom: 2px solid #76ff03;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }
    .output {
        font-size: 18px;
        color: #ffffff;
        font-weight: bold;
        text-align: center;
    }

    .time-input-container {
        display: flex;
        flex-direction: column;
        margin-bottom: 20px;
    }
    .time-input-container label {
        margin-bottom: 8px; /* Espacio entre etiqueta y campo */
    }
    .time-input-container input {
        width: 100%; /* Ajustar al contenedor */
        padding: 8px; /* Espacio interno */
        font-size: 16px;
    }
    .custom-warning {
        background-color: #f8f9fa; /* Color de fondo (gris claro) */
        color: #6c757d; /* Color del texto (gris oscuro) */
        padding: 10px;
        border: 1px solid #d6d8db; /* Borde gris */
        border-radius: 4px;
        font-size: 16px;
        margin-bottom: 10px;
    }
    .stSelectbox > div {
        margin-top: 0 !important; /* Alineación con las descripciones */
    }
    </style>
    """,
    unsafe_allow_html=True
)



mine_images = {
    "Radomiro Tomic": "./Generated_Images/Radomiro-Tomic-.jpeg",
    "Gabriela Mistral": "./Generated_Images/1732572186JfmiH5e9.jpg",
}

allowed_words = [
    "mining", "truck", "excavator", "shovel", "drilling", "haul", "equipment", "ore",
    "safety", "inspection", "downtime", "maintenance", "load", "unload", "shift",
    "operation", "grader", "bulldozer", "water truck", "explosives", "material",
    "transport", "process", "blast", "auxiliary", "pool", "pit", "crusher", "conveyor",
    "grinder", "mill", "refinery", "smelting", "survey", "geology", "rock", "bench",
    "dump", "excavation", "haul road", "stockpile", "reclamation", "monitoring",
    "slurry", "tailings", "screening", "drill rig", "shotcrete", "blasting", "detonation",
    "mineral", "core sample", "ventilation", "underground", "overburden", "grader",
    "dozer", "feeder", "ore pass", "bin", "shaft", "raise", "winze", "crusher feed",
    "ore grade", "mine plan", "cutoff grade", "open pit", "undercut", "horizon",
    "water management", "leach", "heap", "recovery", "processing", "yield", "mill tailings",
    "strip ratio", "mine dump", "bench height", "core logging", "geophysics", "sampling",
    "runoff", "backfill", "cementation", "borehole", "orebody", "dewatering", "grouting",
    "hydrology", "muck", "mine shaft", "pillar", "stope", "decline", "adit", "portal",
    "shaft collar", "ore chute", "skip", "headframe", "hoist", "slurry pump", "deposition",
    "screen mesh", "bucket", "loader", "stockyard", "grading", "scale", "overcut"
]

radomiro_relationships = {
    "CAEX": [
        ("C-01", "CAT 789-D"),
        ("C-02", "CAT 789-D"),
        ("C-03", "CAT 789-D"),
        ("C-04", "CAT 789-D"),
        ("C-05", "CAT 789-D"),
        ("C-06", "CAT 789-D"),
        ("C-07", "CAT 789-C"),
        ("C-08", "CAT 789-C"),
        ("C-09", "CAT 789-C"),
        ("C-10", "CAT 789-C"),
        ("C-11", "CAT 789-C"),
        ("C-12", "CAT 789-C"),
        ("C120", "Kom.930ER"),
        ("C121", "Kom.930ER"),
        ("C122", "Kom.930ER"),
        ("C123", "Kom.930ER"),
        ("C124", "Kom.930ER"),
        ("C125", "Kom.930ER"),
        ("C126", "Kom.930ER"),
        ("C127", "Kom.930ER"),
        ("C128", "Kom.930ER"),
        ("C129", "Kom.930ER"),
        ("C-13", "CAT 789-D"),
        ("C130", "Kom.930ER"),
        ("C-14", "CAT 789-D"),
        ("C-15", "CAT 789-D"),
        ("C-16", "CAT 789-D"),
        ("C-17", "CAT 789-D"),
        ("C801", "DESCARGA"),
        ("C802", "Kom.930E"),
        ("C803", "DESCARGA"),
        ("C804", "DESCARGA"),
        ("C805", "DESCARGA"),
        ("C806", "DESCARGA"),
        ("C807", "DESCARGA"),
        ("C808", "Kom.930E"),
        ("C810", "Kom.930E"),
        ("C811", "Kom.930E"),
        ("C812", "DESCARGA"),
        ("C813", "DESCARGA"),
        ("C814", "Kom.930E"),
        ("C815", "Kom.930E"),
        ("C816", "DESCARGA"),
        ("C817", "Kom.930E"),
        ("C818", "Kom.930EN"),
        ("C819", "Kom.930EN"),
        ("C820", "Kom.930EN"),
        ("C821", "Kom.930EN"),
        ("C822", "Kom.930EN"),
        ("C823", "Kom.930EN"),
        ("C824", "Kom.930EN"),
        ("C825", "Kom.930EN"),
        ("C826", "Kom.930EN"),
        ("C828", "Kom.930ER"),
        ("C829", "Kom.930ER"),
        ("C830", "Kom.930ER"),
        ("C831", "Kom.930ER"),
        ("C832", "Kom.930ER"),
        ("C833", "Kom.930ER"),
        ("C840", "Lieb-T282B"),
        ("C841", "Lieb-T282B"),
        ("C842", "Lieb-T282B"),
        ("C843", "Lieb-T282B"),
        ("C844", "Lieb-T282B"),
        ("C845", "Lieb-T282B"),
        ("C846", "Lieb-T282B"),
        ("C847", "Lieb-T282B"),
        ("C848", "Lieb-T282B"),
        ("C849", "Lieb-T282B"),
        ("C851", "Lieb-T282B"),
        ("C852", "Lieb-T282B"),
        ("C854", "Lieb-T282B"),
        ("C855", "Lieb-T282B"),
        ("C856", "Lieb-T282B"),
        ("C857", "Lieb-T282B"),
        ("C858", "Lieb-T282C1"),
        ("C859", "Lieb-T282C1"),
        ("C860", "Lieb-T282C1"),
        ("C861", "Lieb-T282C1"),
        ("C862", "Lieb-T282C1"),
        ("C863", "Lieb-T282C1"),
        ("C864", "Lieb-T282C1"),
        ("C865", "Lieb-T282C1"),
        ("C866", "Lieb-T282C1"),
        ("C867", "Lieb-T282C1"),
        ("C868", "Lieb-T282C1"),
        ("C869", "Lieb-T282C1"),
        ("C870", "Lieb-T282C1"),
        ("C871", "Lieb-T282C1"),
        ("C901", "Kom.930E-4SE"),
        ("C902", "Kom.930E-4SE"),
        ("C903", "Kom.930E-4SE"),
        ("C904", "Kom.930E-4SE"),
        ("C905", "Kom.930E-4SE"),
        ("C906", "Kom.930E-4SE"),
        ("C907", "Kom.930E-4SE"),
        ("C908", "Kom.930E-4SE"),
        ("C909", "Kom.930E-4SE"),
        ("C910", "Kom.930E-4SE"),
        ("C911", "Kom.930E-4SE"),
        ("C912", "Kom.930E-4SE"),
        ("C913", "Kom.930E-4SE"),
        ("C914", "Kom.930E-4SE"),
        ("C915", "Kom.930E-4SE"),
        ("C916", "Kom.930E-4SE"),
        ("C917", "Kom.930E-4SE"),
        ("C918", "Kom.930E-4SE"),
        ("C919", "Kom.930E-4SE"),
        ("C920", "Kom.930E-4SE"),
        ("C921", "Kom.930E-4SE"),
        ("C922", "Kom.930E-4SE"),
        ("C923", "Kom.930E-4SE"),
        ("C924", "Kom.930E-4SE"),
        ("C925", "Kom.930E-4SE"),
        ("C926", "Kom.930E-4SE"),
        ("C927", "Kom.930E-4SE"),
        ("C928", "Kom.930E-4SE"),
        ("C929", "Kom.930E-4SE"),
        ("C930", "Kom.930E-4SE"),
        ("C931", "Kom.930E-4SE"),
        ("C932", "Kom.930E-4SE"),
        ("C933", "Kom.930E-4SE"),
        ("C934", "Kom.930E-4SE"),
        ("C935", "Kom.930E-4SE"),
        ("RT2", "Kom.930ER"),
        ("RT3", "Kom.930ER"),
        ("RT4", "Kom.930ER"),
        ("RT5", "Kom.930ER"),
    ],
    "CARGUIO":  [
        ("C-21 (SHOVEL)", "CAT 994-F"),
        ("C-22 (ICV)", "CAT 994-F"),
        ("C-23", "CAT 994-F"),
        ("C-24", "CAT 994-F"),
        ("CF-21", "CAT 994-F"),
        ("CF-22", "CAT 994-F"),
        ("FR190", "CAT 992-G"),
        ("FR194", "CAT 992-K"),
        ("PA201", "PH4100XPA"),
        ("PA202", "PH4100XPA"),
        ("PA203", "PH4100XPA"),
        ("PA204", "PH4100XPB"),
        ("PA205", "PH4100XPB"),
        ("PA206", "PH4100XPB"),
        ("PA207", "O&K RH-200"),
        ("PA209", "KOM PC-8000"),
        ("PA210", "PH4100XPCAC"),
        ("PA211", "PH4100XPCAC"),
        ("PA214", "PH4100XPCAC"),
        ("PA250", "CAT 6060-BH"),
        ("PA703", "CF-ELEC-L1400"),
        ("PA708", "CF-ELEC-L1850B"),
        ("PA710", "CF-ELEC-L1850B"),
        ("PA714", "CF-ELEC-L2350"),
        ("PA715", "CF-ELEC-L2350"),
        ("PA716", "CF-ELEC-L1800"),
        ("PA717", "CF-ELEC-L2350"),
        ("PA718", "CF-ELEC-L 2350-GENII"),
        ("PA719", "CF-ELEC-L 2350-GENII"),
        ("PA720", "WA-1200-3"),
        ("PL-001", "LIEB R-9350"),
        ("PL-002", "KOM PC-5500"),
        ("PL-003", "KOM PC-5500"),
        ("RX136", "KOM PC-2000"),
    ],
    "EEAA": [
        ("A504", "REGADOR CAT-777D"),
        ("A505", "REGADOR CAT-777F"),
        ("A506", "REGADOR CAT-777F"),
        ("A507", "REGADOR CAT-777F"),
        ("A508", "REGADOR CAT-777F"),
        ("A509", "REGADOR CAT-777F"),
        ("A510", "REGADOR CAT-777F"),
        ("AL-02", "REGADOR CAT-777F"),
        ("AL-02M", "REGADOR CAT-773F WT"),
        ("AL-03", "REGADOR CAT-773E WT"),
        ("AL-04", "REGADOR CAT-777F"),
        ("AL-302", "REGADOR RENAULT"),
        ("BC208", "BULLDOZER CAT D10T"),
        ("BC215", "BULLDOZER CAT D10T"),
        ("CA-14", "REGADOR SCANNIA P400B"),
        ("CA-21", "MERCEDES/ACTROS 4144K"),
        ("CA-38", "MACK GU-813"),
        ("CA-51", "MACK GU-813"),
        ("EXC-01", "R-944B"),
        ("EXC-02", "R-944B"),
        ("EXC-03", "EXCAVADORA 349 D"),
        ("EXC-04", "EXCAVADORA 349 D"),
        ("EXC-05", "EXCAVADORA 349 D"),
        ("EXC-219", "EXCAVADORA 349 D"),
        ("EXC-611", "CAT 374-F"),
        ("EXC-612", "CAT 374-F"),
        ("GP-215", "TEREX/DEMAG AC160"),
        ("GP-216", "TEREX/RT130"),
        ("GP-217", "TEREX/DEMAG AC160"),
        ("GP-40", "TEREX/RT100"),
        ("GP-41", "TEREX/RT100"),
        ("ICVR-01", "REGADOR CAT-777F"),
        ("ICVR-02", "REGADOR CAT-777F"),
        ("M-01", "CAT-16M"),
        ("M415", "CAT-16M"),
        ("M418", "CAT-24H"),
        ("M419", "CAT-16M"),
        ("M481", "CAT-24M"),
        ("M482", "CAT-24M"),
        ("M483", "CAT-16M"),
        ("M484", "CAT-16M"),
        ("M485", "CAT-16M"),
        ("M486", "CAT-16M"),
        ("M-5952", "NJP/SEMI REMOLQUE"),
        ("M607", "CAT-16M"),
        ("M-7638", "NJP/SEMI REMOLQUE"),
        ("M-DV92", "MITSUBISHI/CANTER"),
        ("M-FJ46", "MACK/GRANITE"),
        ("M-KL15", "RENAULT/C520"),
        ("M-KL17", "RENAULT/C520"),
        ("M-LR52", "MERCEDES/ACTROS 4144K"),
        ("M-LR56", "MERCEDES/ACTROS 4144K"),
        ("M-LR57", "MERCEDES/ACTROS 4144K"),
        ("M-LR58", "MERCEDES/ACTROS 4144K"),
        ("M-LT90", "HYUNDAI/HD 95"),
        ("MN-01", "CAT-16M"),
        ("MN-02", "CAT-16M"),
        ("MN-56", "CAT-16M"),
        ("M-PX87", "MERCEDES/ACTROS 3336"),
        ("PA709", "Cat988"),
        ("PA713", "Cat988"),
        ("PT03", "REGADOR HD785 KOM"),
        ("PT04", "REGADOR HD785 KOM"),
        ("R606", "EXCAVADORA 385 CL"),
        ("R607", "EXCAVADORA 385 C"),
        ("R608", "EXCAVADORA 345 DL"),
        ("R609", "EXCAVADORA 345 DL"),
        ("R657", "BULLDOZER CAT D10T"),
        ("R695", "BULLDOZER CAT D10T"),
        ("R696", "BULLDOZER CAT D10T"),
        ("ROD-532", "RODILLO"),
        ("T-01", "BULL DOZER-D11T"),
        ("T-02", "BULL DOZER-D11T"),
        ("T-03", "BULL DOZER-D11T"),
        ("T-04", "BULLDOZER CAT D10T"),
        ("T-05", "BULLDOZER CAT D10T"),
        ("T-06", "BULLDOZER CAT D10T"),
        ("T-07", "BULLDOZER CAT D10T"),
        ("T-08", "BULLDOZER CAT D9T"),
        ("T-09", "BULLDOZER CAT D10T"),
        ("TO-04", "BULL DOZER-375A"),
        ("TO-05", "BULL DOZER-375A"),
        ("TR408", "BULL DOZER-D11R"),
        ("TR409", "BULL DOZER-D11R"),
        ("TR410", "BULL DOZER-D11R"),
        ("TR424", "TIGRE-854G"),
        ("TR426", "TIGRE-854G"),
        ("TR429", "TIGRE-854K"),
        ("TR430", "TIGRE-854K"),
        ("TR431", "TIGRE-854K"),
        ("TR432", "TIGRE-854K"),
        ("TR433", "TIGRE-854K"),
        ("TR434", "TIGRE-824H"),
        ("TR435", "TIGRE-824H"),
        ("TR436", "TIGRE-824H"),
        ("TR445", "BULL DOZER-D11T"),
        ("TR447", "BULL DOZER-D11T"),
        ("TR448", "BULL DOZER-D11T"),
        ("TR449", "BULL DOZER-D11T"),
        ("TR450", "BULL DOZER-D11T"),
        ("TR451", "BULL DOZER-D11T"),
        ("TR452", "BULL DOZER-D11T"),
        ("TR453", "BULL DOZER-D11T"),
        ("TR454", "BULL DOZER-D11T"),
        ("TR455", "BULL DOZER-D11T"),
        ("TR456", "BULL DOZER-D11T"),
        ("TR457", "BULL DOZER-D11T"),
        ("TR458", "BULL DOZER-D11T"),
        ("TR459", "BULL DOZER-D11T"),
    ],
    "PERFOS": [
        ("P-30", "DRILLTECH D75KS"),
        ("P-31", "DRILLTECH D75KS"),
        ("P-32", "INGERSOLL RAND DM-M2"),
        ("P-33", "INGERSOLL RAND DM-M2"),
        ("P-34", "DRILLTECH D75KS"),
        ("P-35", "INGERSOLL RAND DM-M2"),
        ("P-36", "PV-271"),
        ("PE107", "PITVIPERFL1"),
        ("PE108", "PITVIPERFL1"),
        ("PE109", "PITVIPERFL1"),
        ("PE110", "PITVIPERFL1"),
        ("PE111", "DML"),
        ("PE112", "PITVIPERFL2"),
        ("PE113", "PITVIPERFL2"),
        ("PE114", "PITVIPERFL2"),
        ("PE115", "DML"),
        ("PERFO-01", "Atlas Copco PV-271"),
        ("R01", "ROC-L8.M25"),
        ("R02", "ROC-L8.M25"),
        ("R03", "ROC-L8.M25"),
        ("R04", "ROC-L8.M25"),
        ("R05", "ROC-L8.M25"),
        ("R06", "SMART-ROC"),
        ("R07", "SMART-ROC"),
        ("R08", "SMART-ROC"),
        ("R09", "SMART-ROC"),
        ("R10", "SMART-ROC"),
    ]
}
# Datos dinámicos para las minas
equipment_data = {
    "Radomiro Tomic": {
        "CAEX": {
            "types": ['CAT 789-D', 'CAT 789-C', 'Kom.930ER', 'DESCARGA', 'Kom.930E', 'Kom.930EN','Lieb-T282B', 'Lieb-T282C1', 'Kom.930E-4SE'],
            "ids": ['C-01', 'C-02', 'C-03', 'C-04', 'C-05', 'C-06', 'C-07', 'C-08', 'C-09', 'C-10',
                    'C-11', 'C-12', 'C120', 'C121', 'C122', 'C123', 'C124', 'C125', 'C126', 'C127',
                    'C128', 'C129', 'C-13', 'C130', 'C-14', 'C-15', 'C-16', 'C-17', 'C801', 'C802',
                    'C803', 'C804', 'C805', 'C806', 'C807', 'C808', 'C810', 'C811', 'C812', 'C813',
                    'C814', 'C815', 'C816', 'C817', 'C818', 'C819', 'C820', 'C821', 'C822', 'C823',
                    'C824', 'C825', 'C826', 'C828', 'C829', 'C830', 'C831', 'C832', 'C833', 'C840',
                    'C841', 'C842', 'C843', 'C844', 'C845', 'C846', 'C847', 'C848', 'C849', 'C851',
                    'C852', 'C854', 'C855', 'C856', 'C857', 'C858', 'C859', 'C860', 'C861', 'C862',
                    'C863', 'C864', 'C865', 'C866', 'C867', 'C868', 'C869', 'C870', 'C871', 'C901',
                    'C902', 'C903', 'C904', 'C905', 'C906', 'C907', 'C908', 'C909', 'C910', 'C911',
                    'C912', 'C913', 'C914', 'C915', 'C916', 'C917', 'C918', 'C919', 'C920', 'C921',
                    'C922', 'C923', 'C924', 'C925', 'C926', 'C927', 'C928', 'C929', 'C930', 'C931',
                    'C932', 'C933', 'C934', 'C935', 'RT2', 'RT3', 'RT4', 'RT5']


        },
        "CARGUIO": {
            "types": ['CAT 994-F', 'CAT 992-G', 'CAT 992-K', 'PH4100XPA', 'PH4100XPB', 'O&K RH-200',
                    'KOM PC-8000', 'PH4100XPCAC', 'CAT 6060-BH', 'CF-ELEC-L1400',
                    'CF-ELEC-L1850B', 'CF-ELEC-L2350', 'CF-ELEC-L1800', 'CF-ELEC-L 2350-GENII',
                    'WA-1200-3', 'LIEB R-9350', 'KOM PC-5500', 'KOM PC-2000'],
            "ids": ['C-21 (SHOVEL)', 'C-22 (ICV)', 'C-23', 'C-24', 'CF-21', 'CF-22', 'FR190',
                    'FR194', 'PA201', 'PA202', 'PA203', 'PA204', 'PA205', 'PA206', 'PA207', 'PA209',
                    'PA210', 'PA211', 'PA214', 'PA250', 'PA703', 'PA708', 'PA710', 'PA714', 'PA715',
                    'PA716', 'PA717', 'PA718', 'PA719', 'PA720', 'PL-001', 'PL-002', 'PL-003',
                    'RX136']

        },
        "EEAA": {
            "types": ['REGADOR CAT-777D', 'REGADOR CAT-777F', 'REGADOR CAT-773F WT',
                    'REGADOR CAT-773E WT', 'REGADOR RENAULT', 'BULLDOZER CAT D10T',
                    'REGADOR SCANNIA P400B', 'MERCEDES/ACTROS 4144K', 'MACK GU-813', 'R-944B',
                    'EXCAVADORA 349 D', 'CAT 374-F', 'TEREX/DEMAG AC160', 'TEREX/RT130',
                    'TEREX/RT100', 'CAT-16M', 'CAT-24H', 'CAT-24M', 'NJP/SEMI REMOLQUE',
                    'MITSUBISHI/CANTER', 'MACK/GRANITE', 'RENAULT/C520', 'HYUNDAI/HD 95',
                    'MERCEDES/ACTROS 3336', 'Cat988', 'REGADOR HD785 KOM', 'EXCAVADORA 385 CL',
                    'EXCAVADORA 385 C', 'EXCAVADORA 345 DL', 'RODILLO', 'BULL DOZER-D11T',
                    'BULLDOZER CAT D9T', 'BULL DOZER-375A', 'BULL DOZER-D11R', 'TIGRE-854G',
                    'TIGRE-854K', 'TIGRE-824H'],
            "ids":['A504', 'A505', 'A506', 'A507', 'A508', 'A509', 'A510', 'AL-02', 'AL-02M', 'AL-03',
                    'AL-04', 'AL-302', 'BC208', 'BC215', 'CA-14', 'CA-21', 'CA-38', 'CA-51', 'EXC-01',
                    'EXC-02', 'EXC-03', 'EXC-04', 'EXC-05', 'EXC-219', 'EXC-611', 'EXC-612',
                    'GP-215', 'GP-216', 'GP-217', 'GP-40', 'GP-41', 'ICVR-01', 'ICVR-02', 'M-01',
                    'M415', 'M418', 'M419', 'M481', 'M482', 'M483', 'M484', 'M485', 'M486', 'M-5952',
                    'M607', 'M-7638', 'M-DV92', 'M-FJ46', 'M-KL15', 'M-KL17', 'M-LR52', 'M-LR56',
                    'M-LR57', 'M-LR58', 'M-LT90', 'MN-01', 'MN-02', 'MN-56', 'M-PX87', 'PA709',
                    'PA713', 'PT03', 'PT04', 'R606', 'R607', 'R608', 'R609', 'R657', 'R695', 'R696',
                    'ROD-532', 'T-01', 'T-02', 'T-03', 'T-04', 'T-05', 'T-06', 'T-07', 'T-08', 'T-09',
                    'TO-04', 'TO-05', 'TR408', 'TR409', 'TR410', 'TR424', 'TR426', 'TR429', 'TR430',
                    'TR431', 'TR432', 'TR433', 'TR434', 'TR435', 'TR436', 'TR445', 'TR447', 'TR448',
                    'TR449', 'TR450', 'TR451', 'TR452', 'TR453', 'TR454', 'TR455', 'TR456', 'TR457',
                    'TR458', 'TR459']

        },
        "PERFOS": {
            "types": ['DRILLTECH D75KS', 'INGERSOLL RAND DM-M2', 'PV-271', 'PITVIPERFL1', 'DML',
                    'PITVIPERFL2', 'Atlas Copco PV-271', 'ROC-L8.M25', 'SMART-ROC'],
            "ids": ['P-30', 'P-31', 'P-32', 'P-33', 'P-34', 'P-35', 'P-36', 'PE107', 'PE108', 'PE109',
                    'PE110', 'PE111', 'PE112', 'PE113', 'PE114', 'PE115', 'PERFO-01', 'R01', 'R02',
                    'R03', 'R04', 'R05', 'R06', 'R07', 'R08', 'R09', 'R10']

        }
    },
    "Gabriela Mistral": {
        "CAEX": {
            "ids": ['CE01', 'CE02', 'CE03', 'CE04', 'CE05', 'CE06', 'CE07', 'CE10', 'CE11', 'CE12',
                    'CE13', 'CE14', 'CE15', 'CE16', 'CE17', 'CE18', 'CE19', 'CE20']


        },
        "CARGUIO": {
            "ids": ['PA_01', 'PA_02', 'PC_01', 'CF_01', 'CF_02', 'CF_DEMO']


        },
        "EEAA": {
            "ids": ['CR_01', 'CR_02', 'CR_03', 'EXC01', 'MF_01', 'MF_02', 'MO_02', 'MO_03', 'MO_04',
                    'TN_03', 'TN_04', 'TN_05', 'TO_01', 'TO_02', 'TO_03', 'TO_04', 'TO_05']
        },
        "PERFOS": {
            "ids": ['PD02', 'PE01', 'PE02']

        }
    }
}
#Descripciones de las clases de vehiculos
equipment_descriptions = {
    "CAEX": "Large mining haul trucks used for transporting overburden and ore. These vehicles are critical for moving materials efficiently in mining operations.",
    "CARGUIO": "Loading equipment such as excavators and shovels designed to load materials onto haul trucks or other transport systems.",
    "EEAA": "Auxiliary equipment used in mining operations, such as water trucks, bulldozers, and graders. These support vehicles help maintain operational efficiency and safety.",
    "PERFOS": "Drilling equipment used to create blast holes for explosives or for exploratory drilling to identify ore deposits."
}
#Descripciones de las clases de eventos
class_descriptions = {
    "DO": "Operational downtimes caused by planned activities such as shift changes, training, safety inspections, or other routine procedures. These are scheduled events aimed at maintaining operational standards.",
    "DONP": "Unexpected operational downtimes due to unforeseen events, such as sudden lack of operator availability, equipment misplacement, or situational delays. These require quick intervention to resume operations.",
    "MP": "Scheduled maintenance activities designed to prevent future equipment failures. This includes tasks such as part replacements, inspections, and other proactive measures to ensure reliability.",
    "MC": "Corrective maintenance triggered by unexpected equipment failures. These include breakdowns due to mechanical, electrical, or structural issues that need immediate attention to restore functionality.",
    "DCE": "Downtime caused by external factors beyond operational control. These include weather conditions, social environment disruptions, or other client-independent events affecting the mining process.",
    "DAAR": "Upstream delays or waiting times caused by equipment or processes ahead in the production chain. These impact the smooth flow of operations for the current process or equipment.",
    "DAAB": "Downstream delays or waiting times caused by processes further along the production chain. These occur when subsequent stages of production are not ready or synchronized with the current operations."
}
#Ubicacion para cada imagen TEMPORAL
image_paths = {
    "DO": {
        "PERFOS": "./Generated_Images/DO_PERFOS.png",
        "CAEX": "./Generated_Images/DO_CAEX.png",
        "CARGUIO": "./Generated_Images/DO_CARGUIO.png",
        "EEAA": "./Generated_Images/DO_EEAA.png",
    },
    "DONP": {
        "PERFOS": "./Generated_Images/DONP_PERFOS.png",
        "CAEX": "./Generated_Images/DONP_CAEX.png",
        "CARGUIO": "./Generated_Images/DONP_CARGUIO.png",
        "EEAA": "./Generated_Images/DONP_EEAA.png",
    },
    "MP": {
        "PERFOS": "./Generated_Images/MP_PERFOS.png",
        "CAEX": "./Generated_Images/MP_CAEX.png",
        "CARGUIO": "./Generated_Images/MP_CARGUIO.png",
        "EEAA": "./Generated_Images/MP_EEAA.png",
    },
    "MC": {
        "PERFOS": "./Generated_Images/MC_PERFOS.png",
        "CAEX": "./Generated_Images/MC_CAEX.png",
        "CARGUIO": "./Generated_Images/MC_CARGUIO.png",
        "EEAA": "./Generated_Images/MC_EEAA.png",
    },
    "DCE": {
        "PERFOS": "./Generated_Images/DCE_PERFOS.png",
        "CAEX": "./Generated_Images/DCE_CAEX.png",
        "CARGUIO": "./Generated_Images/DCE_CARGUIO.png",
        "EEAA": "./Generated_Images/DCE_EEAA.png",
    },
    "DAAR": {
        "PERFOS": "./Generated_Images/DAAR_PERFOS.png",
        "CAEX": "./Generated_Images/DAAR_CAEX.png",
        "CARGUIO": "./Generated_Images/DAAR_CARGUIO.png",
        "EEAA": "./Generated_Images/DAAR_EEAA.png",
    },
    "DAAB": {
        "PERFOS": "./Generated_Images/DAAB_PERFOS.png",
        "CAEX": "./Generated_Images/DAAB_CAEX.png",
        "CARGUIO": "./Generated_Images/DAAB_CARGUIO.png",
        "EEAA": "./Generated_Images/DAAB_EEAA.png",
    },
}
# Título principal
st.markdown("<div class='title'>⛏️ Mining Event Classification</div>", unsafe_allow_html=True)
st.markdown("<div class='description'>Find which class type is your event.</div>", unsafe_allow_html=True)

st.markdown('<div class="section-title">Select Mine</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">Select the mining site where the operation is being conducted, such as Radomiro Tomic or Gabriela Mistral.</div>',
    unsafe_allow_html=True
)

# Selección de mina
mine = st.selectbox(
    "",
    options=list(equipment_data.keys()),
    key="mine_select"
)

# Mostrar imagen asociada a la mina seleccionada
if mine in mine_images:
    st.image(
        mine_images[mine],
        use_container_width=True,
        caption=f"Mining operation at {mine}"
    )
else:
    st.warning("No image available for the selected mine.")
# Título y descripción de Equipment Class
st.markdown('<div class="section-title">Equipment Class</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">Choose the broad category of equipment involved in the mining operation, such as trucks (CAEX), loaders (CARGUIO), or drilling rigs (PERFOS).</div>',
    unsafe_allow_html=True
)

equipment_class = st.selectbox(
    "",
    options=[""] + list(equipment_data[mine].keys()),
    key="equipment_class_select"
)

# Opciones dinámicas basadas en Equipment Class
if equipment_class:
    if mine == "Gabriela Mistral":
        st.markdown(
            '<div class="custom-warning">Equipment Type is not applicable for Gabriela Mistral.</div>',
            unsafe_allow_html=True
        )
        equipment_type = None
        equipment_id = st.selectbox(
            "Choose Equipment ID",
            options=[""] + equipment_data[mine][equipment_class].get("ids", []),
            key="equipment_id_select"
        )
    else:
        # Obtener tipos e IDs para otras minas
        types = equipment_data[mine][equipment_class].get("types", [])
        ids = equipment_data[mine][equipment_class].get("ids", [])

        # Título y descripción de Equipment Type
        st.markdown('<div class="section-title">Equipment Type</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-description">Select the specific type or model of equipment within the chosen class, like "CAT 789-D" or "DRILLTECH D75KS".</div>',
            unsafe_allow_html=True
        )
        equipment_type = st.selectbox(
            "",
            options=[""] + types,
            key="equipment_type_select"
        )

        # Filtrar IDs relacionados al tipo seleccionado
        if equipment_type:
            related_ids = [
                equipment_id for equipment_id in ids
                if (equipment_id, equipment_type) in radomiro_relationships.get(equipment_class, [])
            ]
            st.markdown('<div class="section-title">Equipment ID</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-description">Choose the unique identifier for the selected equipment type, representing a specific unit in the operation.</div>',
                unsafe_allow_html=True
            )
            equipment_id = st.selectbox(
                "",
                options=[""] + related_ids,
                key="related_ids_select"
            )
            if not related_ids:
                st.warning(f"No IDs available for the selected type '{equipment_type}'.")
        else:
            st.markdown('<div class="section-title">Equipment ID</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-description">Choose the unique identifier for the selected equipment type, representing a specific unit in the operation.</div>',
                unsafe_allow_html=True
            )
            equipment_id = st.selectbox(
                "",
                options=[""] + ids,
                key="equipment_id_default_select"
            )

# --- Sección: Event Duration ---
st.markdown("<div class='section-header'>Event Duration</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="time-input-container">', unsafe_allow_html=True)
    start_date = st.date_input("Start Date", value=date.today())
    start_time_input = st.text_input("Start Time (HH:MM)", value="08:00", key="start_time")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="time-input-container">', unsafe_allow_html=True)
    end_date = st.date_input("End Date", value=date.today())
    end_time_input = st.text_input("End Time (HH:MM)", value="9:00", key="end_time")
    st.markdown('</div>', unsafe_allow_html=True)

# Validación de formato de hora
try:
    start_time = datetime.strptime(start_time_input, "%H:%M").time()
    end_time = datetime.strptime(end_time_input, "%H:%M").time()

    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(end_date, end_time)

    if end_datetime <= start_datetime:
        st.error("End time must be greater than start time!")
        duration = None
    else:
        duration = (end_datetime - start_datetime).seconds / 60  # Duración en minutos
except ValueError:
    st.error("Please enter valid time in HH:MM format.")
    duration = None


# --- Sección: Additional Information ---
st.markdown("<div class='section-header'>Additional Information</div>", unsafe_allow_html=True)

# Función para validar comentarios
def validate_comment(comment, allowed_words):
    words = comment.lower().split()
    valid_words = [word for word in words if word in allowed_words]
    return len(valid_words) > 0

# Campo de texto con validación en tiempo real
st.markdown("<h3 style='text-align: center;'>Write a comment</h3>", unsafe_allow_html=True)
additional_comment = st.text_area(
    "",
    placeholder="Enter mining-related terms...",
    key="comment"
)

# Validación en tiempo real
if "comment" in st.session_state:
    comment_text = st.session_state.comment.strip()
    if comment_text:
        if validate_comment(comment_text, allowed_words):
            st.markdown(
                "<p style='text-align: center; color: green; font-weight: bold;'>✔ Comment is valid.</p>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<p style='text-align: center; color: red; font-weight: bold;'>✖ Invalid comment. Use mining-related terms.</p>",
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            "<p style='text-align: center; color: orange; font-weight: bold;'>⚠ Please enter a comment.</p>",
            unsafe_allow_html=True
        )

st.markdown("<div class='section-header'>Output</div>", unsafe_allow_html=True)

if st.button("Classify Event"):
    # Usar un spinner para simular una transición
    with st.spinner("Classifying the event, please wait..."):
        import time
        time.sleep(2)  # Simular un pequeño retraso para la transición (puedes ajustar el tiempo)

        # Validaciones de entrada
        if duration is None:
            st.error("Invalid event times. Please fix the inputs.")
        elif not equipment_class:
            st.error("Please select an Equipment Class.")
        else:
            try:
                params = dict(
                    start_time=start_time.strftime("%H:%M:%S"),
                    end_time=end_time.strftime("%H:%M:%S"),
                    equipment_class=equipment_class,
                    equipment=equipment_id,
                    equipment_type=equipment_type,
                    mine_name=mine,
                    nlp_input=additional_comment
                )
                api_url = 'https://coppermining-image-288823311772.europe-west1.run.app/predict'
                response = requests.get(api_url, params=params)

                prediction = response.json()

                # Mostrar resultados
                st.markdown(f"<div class='output'>Prediction: <b>{prediction['answer']}</b></div>", unsafe_allow_html=True)
                explanation = class_descriptions.get(prediction['prediction'], "No explanation available.")
                st.markdown(f"<div class='output'><b>Explanation of the class event:</b> {explanation}</div>", unsafe_allow_html=True)

                # Determinar la URL de la imagen correspondiente
                image_url = image_paths.get(prediction['prediction'], {}).get(equipment_class)
                if image_url:
                    st.image(image_url, caption=f"Visual representation of {prediction['prediction']} - {equipment_class}")
                else:
                    st.warning(f"No image available for the combination: {prediction['prediction']} ({equipment_class}).")

            except Exception as e:
                st.error(f"An error occurred while predicting: {e}")


#Prompt: An ultra-realistic photograph of a mining operation at {mine_name}, capturing a critical moment where a {vehicle_type} is expirencing a {problem_description}. Shot with photographic realism from eye-level POV, the scene conveys true scale and professional mining operations. The {vehicle_type} is prominently featured with clear visibility of affected components, showing authentic surface textures, accumulated dust, and operational wear patterns that reflect its daily use.
#A primary technician wearing full mining safety gear including high-visibility yellow vest, white hard hat with site logo, and steel-toed boots, is methodically inspecting the {vehicle_type}. Their experienced stance and focused attention emphasize the professional nature of the operation. A supervisor stands fifteen feet away, holding a tablet displaying diagnostic data, actively monitoring the situation. A third worker, positioned at ground level near the vehicle, remains ready to assist with specialized tools while maintaining proper safety protocols.
#The environment showcases a professional, active mining site with compact soil ground marked by clear tire impressions. Operational facilities and processing plants create a layered backdrop, with additional mining equipment visible in the middle distance. The maintenance area appears orderly and well-organized, reflecting standard safety practices.
#Natural daylight illuminates the scene, creating soft shadows that add depth without harsh contrasts. A slight mining dust hangs in the air, adding atmospheric perspective, while the sky above remains clear with minimal clouds. The overall atmosphere emphasizes safety, professionalism, and operational efficiency, maintaining photorealistic quality without artistic exaggeration. Every detail, from the workers' coordinated actions to the organized environment, reflects the systematic nature of modern mining operations.
#
#
