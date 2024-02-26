#### . . . Running the GISTIC analyzer
if __name__ == "__main__":
    analyzer = GISTICAnalyzer("/Users/bxz262/Library/CloudStorage/Box-Box/Ziccheddu/final_project_proposal/WORK", ".txt")
    header, _, data = analyzer.file_collapsing("/Users/bxz262/Library/CloudStorage/Box-Box/Ziccheddu/final_project_proposal/WORK/output/collapsed_data.tsv")
    print(header)
    print(data)

    result_df = analyzer.get_alterated_GISTIC_peaks("Genomic_Coordinates_GISTICpeaks.tsv", "/Users/bxz262/Library/CloudStorage/Box-Box/Ziccheddu/final_project_proposal/WORK/output/collapsed_data.tsv", "/Users/bxz262/Library/CloudStorage/Box-Box/Ziccheddu/final_project_proposal/WORK/output/GISTICmatrix.tsv")
    print(result_df.head())

    analyzer.create_heatmap(result_df, "/Users/bxz262/Library/CloudStorage/Box-Box/Ziccheddu/final_project_proposal/WORK/output/heatmap.pdf")

