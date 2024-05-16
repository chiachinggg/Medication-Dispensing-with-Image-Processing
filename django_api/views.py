from io import BytesIO
from rest_framework.response import Response
from rest_framework.decorators import api_view
import base64, os, io
from PIL import Image
from pathlib import Path
import pandas as pd
from skimage import io, filters, transform, img_as_ubyte, img_as_float, color
from skimage.filters import unsharp_mask, threshold_local, threshold_otsu
import matplotlib.pyplot as plt
from skimage import data
import cv2
import numpy as np
import pandas as pd
import pytesseract
import re


@api_view(['GET'])
def test_api(request):
    return Response({"message": "Hello, world!"})

# post request, receive parameters id and name
@api_view(['POST'])
def test_api_post(request):
    id = request.data.get('id')
    name = request.data.get('name')
    return Response({"id": id, "name": name})

# a post request, which used to store the image file as a local file at the server side
@api_view(['POST'])
def store_image(request):

    def preprocess_image(path, filename):

        image = io.imread(path, as_gray=True)

        black_pixels = np.sum(image < 50 / 255.0)  # Convert threshold to range 0-1
        total_pixels = image.size
        black_percentage = black_pixels / total_pixels * 100

        if black_percentage > 40:
            # Invert the image by subtracting each pixel value from 255
            image = 1.0 - image
        
        block_size = 3
        offset = 0.0000001
        thresh_meth = 'gaussian'
        image = threshold_local(image, block_size, thresh_meth, offset)

        image = filters.unsharp_mask(image, radius=3, amount=3.5)

        new_path = "Dataset/temp" + filename + "_processed"

        io.imsave(new_path, image) 
        # os.remove(filename)

        return new_path

    def ocr(file_path):
        img = Image.open(file_path)
        ocr_result = pytesseract.image_to_string(img)
        return ocr_result
    
    def replace_units(text):
    # Replace 'milligram' with 'mg'
        text = re.sub(r'\bmilligram\b', 'mg', text, flags=re.IGNORECASE)
        # Replace 'microgram' with 'mcg'
        text = re.sub(r'\bmicrogram\b', 'mcg', text, flags=re.IGNORECASE)

        text = text.replace(" ", "")
        return text

    def model(path):

        df = pd.read_csv("Dataset_30-4-2024/0 med_data_latest.csv")
        api_list = ["abacavir", "acamprosate", "acarbose", "acetazolamide", "acetic acid-glacial", "aciclovir", "activated charcoal", "adalimumab", "adapalene", "adrenaline", "agomelatine", "alafenamide", "alendronate", "alendronate sodium", "allopurinol", "alprazolam", "alprostadil", "alteplase", "aluminium hydroxide", "amantadine", "amiloride", "amiodarone", "amisulpride", "amitriptyline", "amlodipine", "amlodipine besylate", "ammonium bicarbonate", "amorolfine", "amoxycillin", "amphotericin", "amylmetacresol", "anastrozole", "antazoline phosphate", "apixaban", "apomorphine hemihydrate", "apraclonidine", "arachis oil", "aripiprazole", "aspart protamine", "aspirin", "atenolol", "atorvastatin", "atorvastatin calcium", "atovaquone", "atropine", "atropine sulfate", "azathioprine", "azelastine", "azithromycin", "baclofen", "beclomethasone", "beclomethasone dipropionate", "benserazide", "benzalkonium chloride", "benzhexol", "benzocaine", "benzoic acid", "benzonatate", "benzoyl peroxide", "benzydamine", "benzyl alcohol", "benzyl benzoate", "benzylpenicillin", "betahistine", "betamethasone dipropionate", "betamethasone valerate", "bethanechol", "bictegravir", "bifonazole", "bimatoprost", "biperiden", "bisacodyl", "bisoprolol fumarate", "brimonidine", "bromazepam", "bromhexine", "bromocriptine", "budesonide", "bumetanide", "buprenorphine", "bupropion", "butylated hydroxyanisole", "cabergoline", "caffeine", "calcitriol", "calcium", "calcium carbonate", "calcium chloride", "camphor", "candesartan", "capecitabine", "captopril", "carbamazepine", "carbamide peroxide", "carbidopa", "carbimazole", "carbomer", "carbomer 580", "carbomer 980", "carmellose", "carmellose sodium", "cefaclor", "cefepime", "ceftazidime", "ceftriaxone", "cefuroxime", "celecoxib", "cephalexin", "cetalkonium chloride", "cetirizine", "cetrimide", "cetylpyridium chloride", "chloramphenicol", "chlorbutol", "chlorhexidine", "chlorhexidine gluconate", "chlorpromazine", "cholestyramine", "choline salicylate", "ciclesonide", "ciclosporin", "cinacalcet", "cinchocaine", "ciprofloxacin", "citalopram", "citric acid anhydrous", "clarithromycin", "clavulanic acid", "clindamycin", "clioquinol", "clobazam", "clobetasone butyrate", "clomiphene", "clomipramine", "clonazepam", "clonidine", "clopidogrel", "clotrimazole", "clove bud oil", "coal tar", "cobicistat", "colchicine", "colecalciferol", "crotamiton", "cyclizine", "cyclizine lactate", "cyproheptadine", "cyproterone", "dabigatran", "danaparoid sodium", "desloratadine", "desmopressin", "desogestrel", "desvenlafaxine", "dexamethasone", "dexamphetamine sulphate:dexamphetamine", "dexchlorpheniramine maleate", "dexpanthenol", "dextran", "dextran 70", "dextromethorphan hydrobromide", "dextropropoxyphene", "diazepam", "dichlorobenzyl alcohol", "diclofenac", "diclofenac potassium", "diclofenac sodium", "dicloxacillin", "digoxin", "dihydroergotamine", "diltiazem", "diphenoxylate", "dipyridamole", "disodium etidronate", "disopyramide", "docusate sodium", "dolutegravir", "domperidone", "donepezil", "dorzolamide", "dothiepin", "dothiepin hcl", "doxepin", "doxycycline", "doxylamine succinate", "dulaglutide", "dydrogesterone", "econazole", "econazole nitrate", "efavirenz", "eformoterol", "eformoterol = formoterol", "elvitegravir", "emtricitabine", "enalapril", "enoxaparin", "enoxaparin sodium", "entacapone", "eplerenone", "eprosartan", "eprosartan:mesylate", "erythromycin", "erythromycin ethylsuccinate", "escitalopram", "esomeprazole", "estradiol", "etanercept", "ethanol", "ethinyloestradiol", "ethinyloestriol", "etonogestrel", "eucalyptus oil", "exenatide", "ezetimibe", "famciclovir", "famiciclovir", "famotidine", "felodipine", "fenofibrate", "fentanyl", "ferrous fumarate", "ferrous sulfate", "ferrous sulphate", "fesoterodine", "fexofenadine", "finasteride", "flecainide acetate", "flucloxacillin", "fluconazole", "fludrocortisone", "flumethasone", "flunitrazepam", "fluorometholone", "fluorometholone acetate", "fluorouracil", "fluoxetine", "fluticasone", "fluticasone furoate", "fluticasone propionate", "fluvastatin", "fluvoxamine", "folic acid", "fosinopril", "framycetin", "frusemide", "frusemide = furosemide", "fusidic acid", "gabapentin", "galantamine", "gemfibrozil", "gestodene", "glibenclamide", "gliclazide", "glimepiride", "glipizide", "glycerin", "glycerol", "glyceryl trin", "glyceryl trinitrate", "glycopyrronium", "goserelin", "gramicidin", "guaiphenesin", "haloperidol", "homatropine", "hydralazine", "hydrochlorothiazide", "hydrocortisone", "hydromorphone", "hydroxocobalamin", "hydroxychloroquine", "hyoscine butylbromide", "hyoscine hydrobromide", "hyoscyamine sulfate", "hypromellose", "ibuprofen", "idoxuridine", "imipramine", "imiquimod", "indapamide", "indometacin", "indomethacin = indometacin", "insulin aspart", "insulin detemir", "insulin glargine", "insulin glarine", "insulin isophane", "insulin lispro", "insulin neutral", "ipratroium bromide", "ipratropium", "irbesartan", "iron polymaltose", "iron, vitamin c", "isophane insulin", "isopropyl alcohol", "isosorbide", "isosorbide dinit", "isosorbide mononitrate", "isotretinoin", "ivermectin", "ketoconazole", "ketoprofen", "ketorolac trometamol", "ketotifen", "labetalol", "lactic acid", "lactulose", "lamivudine", "lamotrigine", "lansoprazole", "latanoprost", "leflunomide", "lercanid", "lercanidipine", "letrozole", "levetiracetam", "levocabastine", "levodopa", "levonorgesterol", "levonorgestrel", "levothyroxine", "lignocaine", "lincomycin", "lisinopril", "lispro protamine", "lithium", "lithium carbonate", "loperamide", "loratadine", "lorazepam", "magnesium alginate", "magnesium carbonate", "magnesium hydroxide", "magnesium tricilicate", "maldison", "mebendazole", "medroxyprogesterone", "medroxyprogesterone acetate", "mefenamic acid", "mefloquine", "melatonin", "meloxicam", "memantine", "menthol", "menthol", "mercaptopurine", "mesalazine", "mestranol", "metformin", "metformin xr", "methadone", "methotrexate", "methylphenidate", "methylprednisolone", "metoclopramide", "metolazone", "metoprolol", "metoprolol succinate", "metoprolol tartrate", "metronidazole", "mianserin", "miconazole", "miconazole nitrate", "minocycline", "mirtazapine", "moclobemide", "mometasone furoate", "montelukast", "morphine", "morphine sulfate", "morphine sulphate", "moxonidine", "mupirocin", "mupirocin", "naltrexone", "nan", "naphazoline", "naphazoline hcl", "naproxen", "naproxen sodium", "naratriptan", "nedocromil", "neomycin", "neutral insulin", "nicorandil", "nicotine", "nifedipine", "nitrazepam", "nitrofurantoin", "nizatidine", "norethisterone", "norfloxacin", "nortriptyline", "nystatin", "oestradiol", "oestriol", "oestrogens conjugated", "ofloxacin", "olanzapine", "olmesartan", "olopatadine", "olsalazine sodium", "omeprazole", "ondansetron", "orphenadrine citrate", "ortho-dichlorobenzene", "oseltamivir", "oxazepam", "oxpentifylline", "oxybutynin", "oxycodone", "oxymetazoline", "pantoprazole", "para-dichlorobenzene", "paracetamol", "paroxetine", "pergolide mesylate", "perhexiline maleate", "pericyazine", "permethrin", "peru balsam", "pethidine", "phenazone", "pheniramine maleate", "phenobarbitone", "phenol", "phenoxymethylpenicillin", "phentermine", "phenylephine", "phenylephrine", "phenylephrine", "phenytoin sodium", "pilocarpine", "pimecrolimus", "pindolol", "pioglitazone", "piroxicam", "pizotifen", "podophyllum resin", "poloxamer", "polyethylene glycol", "polysorbate 80", "polyvinyl alcohol", "potassium bicarbonate", "potassium chlor", "potassium chloride", "potassium clavulanic", "potassium dihydrogen phosphate", "povidone", "pramipexole", "prasugrel", "pravastatin", "prazosin", "prednisolone", "prednisolone sodium phosphate", "prednisone", "pregabalin", "primidone", "probenecid", "procaine penicill", "prochlorperazine", "prochlorperazine maleate", "prochlorperazine mesylate", "proguanil", "propantheline", "propranolol", "propylene glycol", "pseudoephedrine", "pseudoephedrine sulfate", "pyrantel", "quetiapine", "quetiapine fumarate", "quinapril", "quinine bisulphate", "quinine sulphate", "rabeprazole", "raloxifene", "ramipril", "ranolazine", "reboxetine", "rilpivirine", "risedronate", "risperidone", "rivaroxaban", "rivastigmine", "rizatriptan", "rosiglitazone", "rosuvastatin", "roxithromycin", "salbutamol", "salicylic acid", "salmeterol", "selegiline", "sennosides", "sertraline", "sevelamer", "sildenafil", "silver sulfadiazine", "simethicone", "simvastatin", "sitagliptin", "sodium alginate", "sodium bicarbonate", "sodium carbonate", "sodium chloride", "sodium citrate", "sodium cromoglycate", "sodium fusidate", "sodium lauryl sulfoacetate", "sodium sulfite", "sodium valproate", "solifenacin", "sorbitol", "sotalol", "sotalol", "spironolactone", "sucralfate", "sulfamethoxazole", "sulfasalazine", "sulindac", "sumatripan", "sumatriptan", "tacrolimus", "tamoxifen", "tamoxifen citrate", "tamsulosin", "tar", "telmisartan", "temazepam", "tenofovir", "tenofovir alafenamide", "terazosin", "terbinafine", "terbinafine", "testosterone", "testosterone undecanoate", "tetrahydrozoline", "tetrahydrozoline", "theophylline", "thyroxine", "tiaprofenic acid", "tibolone", "tilactase", "timolol", "timolol", "tinidazole", "tiotropium", "tobramycin", "tobramycin", "topiramate", "tramadol", "tramazoline", "trandolapril", "tranylcypromine", "travoprost", "trazodone", "tretinoin", "triamcinolone", "triamcinolone acetonide", "triclosan", "triethanolamine lauryl sulfate", "trifluoperazine", "trimeprazine", "trimethoprim", "ulipristal acetate", "ursodeoxycholic", "valaciclovir", "valsartan", "vardenafil", "varenicline", "venlafaxine", "verapamil", "vildagliptin", "vortioxetine", "warfarin sodium", "xylometazoline", "xylometazoline", "zinc oxide", "ziprasidone", "zolmitriptan", "zolpidem", "zopiclone"]

        ocr_results = ocr(file_path)
        ocr_results_list = ocr_results.split("\n\n")
        for j in range(len(ocr_results_list)):
            ocr_results_list[j] = ocr_results_list[j].replace("\n", " ")
        # print(ocr_results_list)
        final_list = [[],""]

        pattern = r'\d+\s?(?:mg|mcg|%w/w|g/g|mg/g|micrograms|milligrams)'

        for item in ocr_results_list:
            match = re.search(pattern, item)
            if match:
                final_list[1] = match.group()
    
            for api in api_list:
                if api in item.lower():
                    if api not in final_list[0]:
                        final_list[0].append(api)
        
        return final_list
    
    success = False
    image_data = request.data.get('image')
    filename = request.data.get('filename')

    if image_data:
        if not os.path.exists('Dataset/temp'):
            os.makedirs('Dataset/temp')
        data = image_data.split("base64,")[1]
        image = Image.open(BytesIO(base64.decodebytes(bytes(data, 'utf-8'))))

        file_path = 'Dataset/temp/' + filename
        image.save(file_path)

        # cc add here

        preprocessed_path = preprocess_image(file_path, filename)
        result = model(preprocessed_path)

        os.remove(preprocessed_path)

        if len(result[0]) > 0 and result[1] != "":
            success = True

    if success:
        return Response({"message": "Image stored successfully", "result": result, "error": None})
    else:
        return Response({"message": "Image cannot be read", "error": "Failed to store image"})



        



