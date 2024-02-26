#### . . . Running the GISTIC analyzer
if __name__ == "__main__":
    analyzer = GISTICAnalyzer("/Users/bxz262/Library/CloudStorage/GoogleDrive-bxz262@miami.edu/My Drive/Bachisio/Documents/PhD_PiBS_CAB/Courses/Courses_Spring2024/PIB_706_Informatics_for_the_Biosciences/Assignments/final_project_proposal/WORK", ".txt")
    header, _, data = analyzer.file_collapsing("collapsed_data.tsv")
    print(header)
    print(data)

    result_df = analyzer.get_alterated_GISTIC_peaks("Genomic_Coordinates_GISTICpeaks.tsv", "collapsed_data.tsv", "GISTICmatrix.tsv")
    print(result_df.head())

    analyzer.create_heatmap(result_df, "heatmap.pdf")
