"""
    git clone https://gitlab.com/22kittens/pyvisjs.git
    cd pyvisjs
    git checkout dev
    py -m venv .venv
    .venv\\Scripts\\activate
    py -m pip install -r requirements.txt
    py -m pip install pandas
    py -m pip install -e .
    py .\\examples\\bluor.py
"""

from pyvisjs import Network, Options
import pandas as pd

d = {
    'Partner1Node': {0: '.GB82BIYS00995636046997', 1: '~035319', 2: '~035319', 3: '~035319', 4: '~035319', 5: '$035796', 6: '$035796', 7: '+039683', 8: '+039683', 9: '$038188', 10: '$035796', 11: '$035796', 12: '$038188', 13: '$038188', 14: '$035796', 15: '$035796', 16: '$038188', 17: '.LT157044060008133181', 18: '$038188', 19: '$035796',20: '.LV02HABA0001308046643', 21: '$038188', 22: '.LV73TREL6060000300000', 23: '.LV64PARX0020150460002'}, 
    'Partner1Name': {0: 'IDZMQKF VTAQD FIZT', 1: 'Eovcetgjh XUH', 2: 'Ptlkwiljr NLB', 3: 'Epnzpsfte QGA', 4: 'Omupwzhae CRD', 5: 'Xymtvvn Qwbw', 6: 'Nlirrns Xgbn', 7: 'Cthgclqpkuo Qme Scraqzc', 8: 'Gkckdqqrmbz Kay Xbaxshx', 9: 'Zebišwvnesx Ipsagxtn', 10: 'Rxusccs Dmup', 11: 'Dpjylyn Frsw', 12: 'Kwwmšapwvjz Sdjinvny', 13: 'Czlušzmqcrs Obsxluzb', 14: 'Jndfang Espa', 15: 'Ueskswk Ugxb', 16: 'Zdovšgqkycy Wadpvapx', 17: 'GL JEJGF FJYIURK NFFXTI', 18: 'Begxšmibcet Nxhvsqsg', 19: 'Uuaqwxw Mcnj', 20: 'LYMKKE OJP', 21: 'Sxdbšhxpgrm Gvivwftj', 22: 'EQNUWF TSGHWWU (RNA)', 23: 'XJL SWFAEL FDNPNG'}, 
    'Partner2Node': {0: '~035319', 1: '$038188', 2: '$035796', 3: '.MR1300001000010000321100839', 4: '+LV33TREL1060000300000', 5: '$042326', 6: '$062128', 7: '$038188', 8: '$035796', 9: '.ES8700494601472016087320', 10: '$093242', 11: '.GB08BIYS00995665610437', 12: '.GB08BIYS00995665610437', 13: '+039683', 14: '+039683',15: '$085649', 16: '.LV37HABA0551044073241', 17: '$035796', 18: '^CARDS', 19: '.LV12UNLA0050007588848', 20: '$035796', 21: '$048787', 22: '$035796', 23: '$035796'}, 
    'Partner2Name': {0: 'Yqlyoqoxr KRV', 1: 'Hxmkšcnjllw Oorapqni', 2: 'Pdbvpgx Vbrw', 3: 'MMWYVN WYUUGT TBURACRXFRF', 4: '   EQTNOL HYNI', 5: 'Ppwzps qufqzo VEE', 6: 'QVQPRNBH"UR NBWOWNP"', 7: 'Nvwišwtepas Vtaigtdk', 8: 'Aetffru Jimy', 9: 'OJB BOSUYFYH N.O', 10: 'VWMP XTSXD 8 MFL', 11: 'GCYEF  HJXGVFQ JME', 12: 'VJIJH  KLGCFIO JLL', 13: 'Pgmfrpsmdzf Vkb Izxhuhp', 14: 'Rdpghgvyudx Xdj Yxyisjs', 15: 'JPFVSYF SHOIURQ', 16: 'DUU EJLJHE FTFAI', 17: 'Mgshthq Kdrr', 18: 'GLCCO', 19: 'AXXSIHXX VXBTCGZN LFŠUUVWBLME GKAFGPE TDFLSTNSD DOWŠXAB HQXORTFD', 20: 'Biiwaki Gype', 21: 'Kxklšdqeady Hebuocp', 22: 'Hjzdjdz Cepy', 23: 'Juonqyu Nnci'}, 
    'Turnover': {0: 25024001.48, 1: 11014268.92,2: 11000000.0, 3: 4959267.39, 4: 2609646.64, 5: 2376555.36, 6: 1789400.0, 7: 1650000.0, 8: 1650000.0, 9: 1270000.0, 10: 938429.28, 11: 837500.0, 12: 834500.0, 13: 830000.0, 14: 825000.0, 15: 803400.0, 16: 650000.0, 17: 222700.24, 18: 171058.23, 19: 167553.86, 20: 151131.03, 21: 136400.0, 22: 130630.64, 23: 110708.42}, 
    'Percent': {0: '100%, 25.0M', 1: '31%, 11.0M', 2: '31%, 11.0M', 3: '14%, 5.0M', 4: '7%, 2.6M', 5: '2.4M', 6: '1.8M', 7: '1.6M', 8: '1.6M', 9: '1.3M', 10: '938.4k', 11: '837.5k', 12: '834.5k', 13: '830.0k', 14: '825.0k', 15: '803.4k', 16: '650.0k', 17: '222.7k', 18: '171.1k', 19: '167.6k', 20: '151.1k', 21: '136.4k', 22: '130.6k', 23: '110.7k'}, 
    'Categories': {0: 'unclass.', 1: 'unclass.', 2: 'unclass.', 3: 'unclass.', 4: 'unclass.', 5: 'loans 99%', 6: 'unclass.', 7: 'unclass.', 8: 'unclass.', 9: 'unclass.', 10: 'unclass.', 11: 'loans 99%', 12: 'loans 99%', 13: 'loans 99%', 14: 'loans 100%', 15: 'unclass.', 16: 'loans 100%', 17: 'unclass.', 18: 'unclass.', 19: 'unclass.', 20: 'loans 14%', 21: 'unclass.', 22: 'unclass.', 23: 'unclass.'}, 
    'Countries': {0: 'GB', 1: 'LV', 2: 'LV', 3: 'MR', 4: 'LV', 5: 'LV', 6: 'LV', 7: '  ', 8: '  ', 9: 'ES', 10: 'LV', 11: 'GB', 12: 'GB', 13: 'GB', 14: 'GB', 15: 'LV', 16: 'LV', 17: 'LT', 18: 'LVA', 19: 'LV', 20: 'LV', 21: 'LV', 22: 'LV', 23: 'LV'}, 
    'from_id': {0: 'GB82BIYS00995636046997', 1: '035319', 2: '035319', 3: '035319', 4: '035319', 5: '035796', 6: '035796', 7: '039683', 8: '039683', 9: '038188', 10: '035796', 11: '035796', 12: '038188', 13: '038188', 14: '035796', 15: '035796', 16: '038188', 17: 'LT157044060008133181', 18: '038188', 19: '035796', 20: 'LV02HABA0001308046643', 21: '038188', 22: 'LV73TREL6060000300000', 23: 'LV64PARX0020150460002'}, 
    'to_id': {0: '035319', 1: '038188', 2: '035796', 3: 'MR1300001000010000321100839', 4: 'LV33TREL1060000300000', 5: '042326', 6: '062128', 7: '038188', 8: '035796', 9: 'ES8700494601472016087320', 10: '093242', 11: 'GB08BIYS00995665610437', 12: 'GB08BIYS00995665610437', 13: '039683', 14: '039683', 15: '085649', 16: 'LV37HABA0551044073241', 17: '035796', 18: 'CARDS', 19: 'LV12UNLA0050007588848', 20: '035796', 21: '048787', 22: '035796', 23: '035796'}, 
    'id': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 13, 13: 14, 14: 15, 15: 16, 16: 17, 17: 18, 18: 19, 19: 20, 20: 21, 21: 22, 22: 23, 23: 24}
}

df = pd.DataFrame(d)

def get_color_and_shape(node, country):
# The types with the label inside of it are: ellipse, circle, database, box, text. 
# The ones with the label outside of it are: image, circularImage, diamond, dot, star, triangle, triangleDown, square and icon.

    BIG_SIZE = 80
    MEDIUM_SIZE = 50
    SMALL_SIZE = 20
    EXTRA_SMALL_SIZE = 20

    ch = node[0]

    if ch == "~":
        color = "orange"
        shape = None
        size = BIG_SIZE
        second_line = "\n" + node[1:]
    elif ch == "$":
        color = "#4eba3f"
        shape = "circle" # circle | dot
        size = SMALL_SIZE
        second_line = "\n" + node[1:]
    elif ch == ".":
        color = "#54bede"
        shape = "box" #square | box
        size = SMALL_SIZE
        second_line = " | " + country
    elif ch == "^":
        color = "#F02B4B"
        shape = "triangle"
        size = SMALL_SIZE
        second_line = ""
    elif ch == "`":
        color = "#DF7DEC"
        shape = "diamond"
        size = SMALL_SIZE
        second_line = ""
    elif ch == "+":
        color = "black"
        shape = "dot"
        size = EXTRA_SMALL_SIZE
        second_line = "\n" + node[1:]
    else:
        color = "lime"
        shape = "dot"
        size = SMALL_SIZE
        second_line = "\n" + node[1:]

    return (color, shape, size, second_line)

####################
try_gummy = True  
####################
springConstant = (0.05 if try_gummy else 0)
damping = (0.05 if try_gummy else 0)

options = Options("800px", "1300px")
options \
    .set_configure(enabled=False) \
    .set_interaction(dragNodes=True, hideEdgesOnDrag=False, hideNodesOnDrag=False)
options.nodes \
    .set_font(face="JetBrains Mono")
options.edges \
    .set_color(inherit=True) \
    .set_font(face="JetBrains Mono") \
    .set_smooth(type="dynamic", enabled=True) \
    .set(arrows="to", arrowStrikethrough=False)
options.physics \
    .set(enabled=True) \
    .set_barnesHut(avoidOverlap=0, centralGravity=0.3, damping=damping, gravitationalConstant=-2750, springConstant=springConstant, springLength=250) \
    .set_stabilization(enabled=True, fit=True, iterations=1000, onlyDynamicEdges=False, updateInterval=50)

net = Network(options=options)

for (index, row) in df.iterrows():
    (color1, shape1, size1, second_line1) = get_color_and_shape(row["Partner1Node"], row["Countries"])
    (color2, shape2, size2, second_line2) = get_color_and_shape(row["Partner2Node"], row["Countries"])

    node1, node2 = row["Partner1Node"][1:], row["Partner2Node"][1:]

    net.add_node(
        node_id = node1, 
        label = row["Partner1Name"].replace("  ", "").replace(" ", "\n") + second_line1, 
        shape = shape1,
        color = color1,
        size = size1,
        cid = None,
        partner_name = row["Partner1Name"]
    )

    net.add_node(
        node_id = node2, 
        label = row["Partner2Name"].replace("  ", "").replace(" ", "\n") + second_line2, 
        shape = shape2,
        color = color2,
        size = size2,
        cid = None,
        partner_name = row["Partner2Name"]
    )

    net.add_edge(
        node1
        , node2
        , value=row["Turnover"]
        , arrowStrikethrough=False
        , label=row["Percent"] + "\n" + row["Categories"]
        , category = row["Categories"].split()[0] # only the first category without percentage
        , row_id = row["id"]
        , partner1_name = row["Partner1Name"]
        , partner2_name = row["Partner2Name"]
        , country = row["Countries"]
    )



net.render_tom_template(
                    title="035319 2023-06-01 / 2023-12-31",
                    open_in_browser=True,
                    enable_highlighting=True, 
                    edge_filtering=["country", "category"],
                    node_filtering=["partner_name"]
                    )

#net.show("example2.html")