import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class GISTICAnalyzer:
    def __init__(self, working_dir, file_pattern):
        self.working_dir = working_dir
        self.file_pattern = file_pattern

    def file_collapsing(self, output_collapsed_file):
        os.chdir(self.working_dir)
        lst = [file for file in os.listdir() if file.endswith(self.file_pattern)]
        header = None
        new_data = []
        first_file_processed = False

        for file_name in lst:
            with open(file_name, 'r') as file:
                lines = file.readlines()

                if not first_file_processed:
                    header = lines.pop(0).strip()
                    new_header = header + "\t" + "sample"
                    first_file_processed = True
                else:
                    lines.pop(0)
                new_data.extend(lines)

            for i in range(len(new_data)):
                new_data[i] = new_data[i].strip("\n") + "\t" + file_name + "\n"

        DEF = []
        for row in new_data:
            DEF.append(row.strip("\t"))

        # Write the object
        with open(output_collapsed_file, 'w') as f:
            f.write(new_header + "\n")
            f.write("".join(DEF))

        return new_header, "\n", DEF

    def get_alterated_GISTIC_peaks(self, file1_path, file2_path, output_file):
        file1_df = pd.read_csv(file1_path, delimiter="\t")
        file2_df = pd.read_csv(file2_path, delimiter="\t", index_col=False)

        # Merge the two dataframes based on "chr"
        merged_df = pd.merge(file1_df, file2_df, on=["chr"], how="inner")

        # Apply filters
        merged_df_1 = merged_df[(merged_df['start_y'] <= merged_df['start_x']) &
                                (merged_df['end_y'] <= merged_df['end_x']) &
                                (merged_df['end_y'] > merged_df['start_x'])]

        merged_df_2 = merged_df[(merged_df['start_y'] >= merged_df['start_x']) &
                                (merged_df['end_y'] >= merged_df['end_x']) &
                                (merged_df['start_y'] < merged_df['end_x'])]

        merged_df_3 = merged_df[(merged_df['start_y'] >= merged_df['start_x']) &
                                (merged_df['end_y'] <= merged_df['end_x'])]

        merged_df_4 = merged_df[(merged_df['start_y'] < merged_df['start_x']) &
                                (merged_df['end_y'] > merged_df['end_x'])]

        merged_df_all = pd.concat([merged_df_1, merged_df_2, merged_df_3, merged_df_4], ignore_index=True)

        print("Merged DataFrame:")
        print(merged_df_all.head())

        # Get abnormal peaks
        abnormal_peaks_dict = {}
        for index, row in merged_df_all.iterrows():
            sample = row['sample']
            peak = row['peak']
            if sample not in abnormal_peaks_dict:
                abnormal_peaks_dict[sample] = set()
            if peak.startswith('Amp_') and row['tcn.em'] > 2 and row['lcn.em'] == 1:
                abnormal_peaks_dict[sample].add(peak)
            elif peak.startswith('Del_') and ((row['tcn.em'] < 2 and row['lcn.em'] == 0) or (row['tcn.em'] >= 2 and row['lcn.em'] == 0)):
                abnormal_peaks_dict[sample].add(peak)

        print("\nAbnormal Peaks Dictionary:")
        print(abnormal_peaks_dict)

        # Create a dictionary to store abnormal status for each sample and peak
        result_dict = {}
        for sample, abnormal_peaks in abnormal_peaks_dict.items():
            result_dict[sample] = {}
            for peak in abnormal_peaks:
                result_dict[sample][peak] = 1
            # Fill in 0 for non-abnormal peaks
            for peak in set(merged_df['peak']) - abnormal_peaks:
                if peak not in result_dict[sample]:
                    result_dict[sample][peak] = 0

        # Convert the dictionary into a pandas dataframe
        result_df = pd.DataFrame(result_dict).fillna(0)

         # Save the result_df dataframe to a tsv file
        result_df.to_csv(output_file, sep="\t", index=True)

        return result_df

    def create_heatmap(self, abnormal_df, output_file):
        # Create a heatmap
        plt.figure(figsize=(10, 6))  # Set the figure size
        sns.heatmap(abnormal_df, cmap='coolwarm', cbar=True, linewidths=0.5, linecolor='black')
        plt.title('Abnormal Peaks Heatmap')  # Set the title of the plot
        plt.xlabel('Samples')  # Set the label for x-axis
        plt.ylabel('Abnormal Peaks')  # Set the label for y-axis
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.tight_layout()  # Adjust layout to prevent clipping of labels

        # Save the plot to a PDF file
        plt.savefig(output_file)

        # Save the plot to a PDF file
        plt.savefig(output_file)
