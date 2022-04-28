import json

def generate_scores_from_ratios(
    INPUT_PROPERTY = json.load(open("./datasets/sorted_property.json")),
    INPUT_VIOLENT = json.load(open("./datasets/sorted_violent.json")),
    INPUT_ALL = json.load(open("./datasets/sorted_all.json")),
    INPUT_PROPERTY_PROJECTED = json.load(open("./datasets/sorted_property_projected.json")),
    INPUT_VIOLENT_PROJECTED = json.load(open("./datasets/sorted_violent_projected.json")),
    INPUT_ALL_PROJECTED = json.load(open("./datasets/sorted_all_projected.json")),
    OUTPUT_FILE_DIR = "./datasets/scores.json"
):
    OUTPUT_FILE = {}
    i = 0
    size = len(INPUT_PROPERTY)
    for tuple in INPUT_PROPERTY:
        if tuple[1] not in OUTPUT_FILE:
            OUTPUT_FILE[tuple[1]] = {}
        
        OUTPUT_FILE[tuple[1]][tuple[0]] = {
            "violent_crime_score": 0,
            "property_crime_score": 0,
            "all_crime_score": 0,
            "safe-living-score": 0
        }

        OUTPUT_FILE[tuple[1]][tuple[0]]["property_crime_score"] = (i / size * 100)

        i += 1
        
    i = 0
    size = len(INPUT_VIOLENT)
    for tuple in INPUT_VIOLENT:
        OUTPUT_FILE[tuple[1]][tuple[0]]["violent_crime_score"] = (i / size * 100)

        i += 1
    
    i = 0
    size = len(INPUT_ALL)
    for tuple in INPUT_ALL:
        OUTPUT_FILE[tuple[1]][tuple[0]]["all_crime_score"] = (i / size * 100)
        OUTPUT_FILE[tuple[1]][tuple[0]]["safe-living-score"] = 100 - (i / size * 100)

        i += 1
    


    i = 0
    size = len(INPUT_PROPERTY_PROJECTED)
    for tuple in INPUT_PROPERTY_PROJECTED:

        OUTPUT_FILE[tuple[1]][tuple[0]]["property_crime_score_projected"] = (i / size * 100)

        i += 1
        
    i = 0
    size = len(INPUT_VIOLENT_PROJECTED)
    for tuple in INPUT_VIOLENT_PROJECTED:
        OUTPUT_FILE[tuple[1]][tuple[0]]["violent_crime_score_projected"] = (i / size * 100)

        i += 1
    
    i = 0
    size = len(INPUT_ALL_PROJECTED)
    for tuple in INPUT_ALL_PROJECTED:
        OUTPUT_FILE[tuple[1]][tuple[0]]["all_crime_score_projected"] = (i / size * 100)
        OUTPUT_FILE[tuple[1]][tuple[0]]["safe-living-score_projected"] = 100 - (i / size * 100)

        i += 1
    
    with open(OUTPUT_FILE_DIR, "w") as outfile:
        json.dump(OUTPUT_FILE, outfile)
    
    print("Done!")
    
    
    
    



def main():
    generate_scores_from_ratios()


if __name__ == "__main__":
    main()