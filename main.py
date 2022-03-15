import glob
from classesMICUSP import BatchInformation, TaggedFile
import webbrowser
filesPath = glob.glob("./taggedfilesMICUSP/*.txt")

x = BatchInformation(filesPath)
x.run()
print(x.dfFinal)
print(x.log)

x.dfFinal.to_csv("resultadoMicusp.csv")
x.dfFinal.to_excel("resultado_Micusp_xlsx.xlsx")

# micusp1 = x.dfFinal.iloc[0:800000,:]
# micusp2 = x.dfFinal.iloc[800000:1600000,:]
# micusp3 = x.dfFinal.iloc[1600000:,:]

# micusp1.to_excel("micusp_1.xlsx")
# micusp2.to_excel("micusp_2.xlsx")
# micusp3.to_excel("micusp_3.xlsx")
