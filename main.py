# Get a list of variants as input and return a network of associations between variants
# and associated genes in simple interaction format to be imported in Cytoscape. Then
# we can add Wikipathway terms from an xgmml file to the initial network using CyTargetLinker app.

from biomart import BiomartServer
import mygene

mg = mygene.MyGeneInfo()

vars = open("variant_list.txt", "r")

server = BiomartServer("http://uswest.ensembl.org/biomart")
hsapiens_snp = server.datasets['hsapiens_snp']

def geneId(var):
    search_res = hsapiens_snp.search({
        'filters': {
            'snp_filter': var
        },
        'attributes': [
            'ensembl_gene_stable_id'
        ]
        })
    result = search_res.iter_lines()
    return next(result).decode('utf-8')

def id2Symbol(geneId):
    gene = mg.getgene(geneId, fields=['symbol'])
    return gene.get('symbol')

sif = open("sifFile.sif", "w")
for var in vars:
    variant = var.strip()
    gene_id = geneId(variant)
    gene_symbol = id2Symbol(gene_id)
    sif.write(variant + "\tvg\t" + gene_symbol + "\n")
sif.close()
