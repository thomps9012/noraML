import pandas as pd
from pprint import pprint
from yattag import Doc
from operator import itemgetter
import sys



class RetrieveRecords:
    def getRecords():
        csv_df = pd.read_csv("NOMS_entered_interviews.csv")
        kept_columns = ["ConsumerID", "Assessment", "Gender",
                        "SexualIdentity", "NightsHomeless", "Housing", "Employment", "InterviewDate"]
        dropping_columns = []
        for col in csv_df:
            if col not in kept_columns:
                dropping_columns.append(col)
        post_drop = csv_df.drop(columns=dropping_columns)
        return post_drop
    
    def confirmData(data):
        file_name = data["file_name"]
        records = data["records"]
        confirm = input(bcolors.HEADER+"Data Looks OK?\n"+bcolors.WARNING+"Y or N\n"+bcolors.ENDC)
        if confirm == "N":
            RetrieveRecords.confirmData(RetrieveRecords.getRecords(file_name))
        else:
            return records

class FormatCounts:
    def returnCount(df):
        return df["ConsumerID"].count()

    def filterInterviewType(type, records):
        if type == "intake":
            interviews = records.where(records["Assessment"] == 600)
            return {
                "records": interviews,
                "count": FormatCounts.returnCount(interviews)
            }
        if type == "followup":
            interviews = records.where(records["Assessment"] == 601)
            return {
                "records": interviews,
                "count": FormatCounts.returnCount(interviews)
            }
        if type == "second_followup":
            interviews = records.where(records["Assessment"] == 602)
            return {
                "records": interviews,
                "count": FormatCounts.returnCount(interviews)
            }
        if type == "discharge":
            interviews = records.where(records["Assessment"] == 699)
            return {
                "records": interviews,
                "count": FormatCounts.returnCount(interviews)
            }

    def genderCount(type_records):
        male = type_records.where(type_records["Gender"] == 1)
        female = type_records.mask(type_records["Gender"] == 1)
        hetero = type_records.where(type_records["SexualIdentity"] == 1)
        nonhetero = type_records.mask(type_records["SexualIdentity"] == 1)
        nonhetero_male = male.mask(male["SexualIdentity"] == 1)
        return {
            "male": FormatCounts.returnCount(male),
            "female": FormatCounts.returnCount(female),
            "heterosexual": FormatCounts.returnCount(hetero),
            "non-heterosexual": FormatCounts.returnCount(nonhetero),
            "male-non-heterosexual": FormatCounts.returnCount(nonhetero_male),
        }

    def employmentCount(type_records):
        removed_outliers = type_records.mask(type_records["Employment"] == -1)
        outliers = type_records.where(type_records["Employment"] == -1)
        full_time_employed = removed_outliers.where(
            removed_outliers["Employment"] == 1)
        part_time_employed = removed_outliers.where(
            removed_outliers["Employment"] == 2)
        unemployed_searching = removed_outliers.where(
            removed_outliers["Employment"] == 3)
        unemployed_not_looking = removed_outliers.where(
            removed_outliers["Employment"] == 7)
        unemployed_disability = removed_outliers.where(
            removed_outliers["Employment"] == 4)
        retired = removed_outliers.where(
            removed_outliers["Employment"] == 6)
        return {
            "outliers": FormatCounts.returnCount(outliers),
            "employment_records": FormatCounts.returnCount(removed_outliers),
            "disability": FormatCounts.returnCount(unemployed_disability),
            "retired": FormatCounts.returnCount(retired),
            "full_time": FormatCounts.returnCount(full_time_employed),
            "part_time": FormatCounts.returnCount(part_time_employed),
            "employed": FormatCounts.returnCount(full_time_employed)+FormatCounts.returnCount(part_time_employed),
            "unemployed_searching": FormatCounts.returnCount(unemployed_searching),
            "unemployed_not_looking": FormatCounts.returnCount(unemployed_not_looking),
            "unemployed": FormatCounts.returnCount(unemployed_searching) + FormatCounts.returnCount(unemployed_not_looking),
        }

    def housingCount(type_records):
        housed = type_records.mask(type_records["Housing"] == 8)
        homeless = type_records.where(type_records["Housing"] == 8)
        homeless_nights = type_records.where(
            type_records["NightsHomeless"] > 0)
        homeless_declared = FormatCounts.returnCount(homeless)
        homeless_nights_declared = FormatCounts.returnCount(homeless_nights)
        homeless_count = homeless_declared if homeless_declared > homeless_nights_declared else homeless_nights_declared
        return {
            "housed": FormatCounts.returnCount(housed),
            "homeless": homeless_count,
        }

    def logInfo(type, records):
        filtered_records = FormatCounts.filterInterviewType(
            type=type, records=records)
        print("TOTAL "+type.upper())
        type_records = filtered_records["records"]
        type_count = filtered_records["count"]
        print("Total", type_count)
        print("----------------------------------------------")
        pprint(FormatCounts.genderCount(type_records=type_records))
        pprint(FormatCounts.employmentCount(type_records=type_records))
        pprint(FormatCounts.housingCount(type_records=type_records))
        print("")

    def returnData(type, records):
        filtered_records = FormatCounts.filterInterviewType(
            type=type, records=records)
        print("TOTAL "+type.upper())
        type_records = filtered_records["records"]
        type_count = filtered_records["count"]
        gender_count = FormatCounts.genderCount(type_records=type_records)
        female, male, heterosexual, non_heterosexual, male_non_heterosexual = itemgetter(
            "female", "male", "heterosexual", "non-heterosexual", "male-non-heterosexual")(gender_count)
        employment_count = FormatCounts.employmentCount(
            type_records=type_records)
        employment_records, disability, retired, full_time, part_time, employed, unemployed_searching, unemployed_not_looking, unemployed = itemgetter(
            "employment_records", "disability", "retired", "full_time", "part_time", "employed", "unemployed_searching", "unemployed_not_looking", "unemployed")(employment_count)
        housing_count = FormatCounts.housingCount(type_records=type_records)
        housed, homeless = itemgetter("housed", "homeless")(housing_count)
        if int(employment_records) == 0:
            return {
                "title": "All "+" ".join(type.upper().split("_"))+" Records",
                "data": [
                    {
                        "identifier": "Female",
                        "number": female,
                        "total_count": type_count,
                        "percentage": round(female/type_count*100, 2),
                    },
                    {
                        "identifier": "Male",
                        "number": male,
                        "total_count": type_count,
                        "percentage": round(male/type_count*100, 2),
                    },
                    {
                        "identifier": "Heterosexual",
                        "number": heterosexual,
                        "total_count": type_count,
                        "percentage": round(heterosexual/type_count*100, 2),
                    },
                    {
                        "identifier": "Non-Heterosexual",
                        "number": non_heterosexual,
                        "total_count": type_count,
                        "percentage": round(non_heterosexual/type_count*100, 2),
                    },
                    {
                        "identifier": "Male Non-Hetersexual",
                        "number": male_non_heterosexual,
                        "total_count": type_count,
                        "percentage": round(male_non_heterosexual/type_count*100, 2),
                    },
                    {
                        "identifier": "Employed Part Time",
                        "number": "MISSING DATA",
                        "total_count": "MISSING DATA",
                        "percentage": "MISSING DATA"
                    },
                    {
                        "identifier": "Employed Full Time",
                        "number": "MISSING DATA",
                        "total_count": "MISSING DATA",
                        "percentage": "MISSING DATA"
                    },
                    {
                        "identifier": "Employed",
                        "number": "MISSING DATA",
                        "total_count": "MISSING DATA",
                        "percentage": "MISSING DATA"
                    },
                    {
                        "identifier": "Receiving Disability",
                        "number": "MISSING DATA",
                        "total_count": "MISSING DATA",
                        "percentage": "MISSING DATA"
                    },
                    {
                        "identifier": "Retired",
                        "number": "MISSING DATA",
                        "total_count": "MISSING DATA",
                        "percentage": "MISSING DATA"
                    },
                    {
                        "identifier": "Unemployed Searching for Work",
                        "number": "MISSING DATA",
                        "total_count": "MISSING DATA",
                        "percentage": "MISSING DATA"
                    },
                    {
                        "identifier": "Unemployed Not Searching",
                        "number": "MISSING DATA",
                        "total_count": "MISSING DATA",
                        "percentage": "MISSING DATA"
                    },
                    {
                        "identifier": "Unemployed",
                        "number": "MISSING DATA",
                        "total_count": "MISSING DATA",
                        "percentage": "MISSING DATA"
                    },
                    {
                        "identifier": "Housed",
                        "number": housed,
                        "total_count": type_count,
                        "percentage": round(housed/type_count*100, 2)
                    },
                    {
                        "identifier": "Homeless",
                        "number": homeless,
                        "total_count": type_count,
                        "percentage": round(homeless/type_count*100, 2)
                    },
                ]
            }
        else:
            return {
                "title": "All "+" ".join(type.upper().split("_"))+" Records",
                "data": [
                    {
                        "identifier": "Female",
                        "number": female,
                        "total_count": type_count,
                        "percentage": round(female/type_count*100, 2),
                    },
                    {
                        "identifier": "Male",
                        "number": male,
                        "total_count": type_count,
                        "percentage": round(male/type_count*100, 2),
                    },
                    {
                        "identifier": "Heterosexual",
                        "number": heterosexual,
                        "total_count": type_count,
                        "percentage": round(heterosexual/type_count*100, 2),
                    },
                    {
                        "identifier": "Non-Heterosexual",
                        "number": non_heterosexual,
                        "total_count": type_count,
                        "percentage": round(non_heterosexual/type_count*100, 2),
                    },
                    {
                        "identifier": "Male Non-Hetersexual",
                        "number": male_non_heterosexual,
                        "total_count": type_count,
                        "percentage": round(male_non_heterosexual/type_count*100, 2),
                    },
                    {
                        "identifier": "Employed Part Time",
                        "number": part_time,
                        "total_count": employment_records,
                        "percentage": round(part_time/employment_records*100, 2)
                    },
                    {
                        "identifier": "Employed Full Time",
                        "number": full_time,
                        "total_count": employment_records,
                        "percentage": round(full_time/employment_records*100, 2)
                    },
                    {
                        "identifier": "Employed",
                        "number": employed,
                        "total_count": employment_records,
                        "percentage": round(employed/employment_records*100, 2)
                    },
                    {
                        "identifier": "Receiving Disability",
                        "number": disability,
                        "total_count": employment_records,
                        "percentage": round(disability/employment_records*100, 2)
                    },
                    {
                        "identifier": "Retired",
                        "number": retired,
                        "total_count": employment_records,
                        "percentage": round(retired/employment_records*100, 2)
                    },
                    {
                        "identifier": "Unemployed Searching for Work",
                        "number": unemployed_searching,
                        "total_count": employment_records,
                        "percentage": round(unemployed_searching/employment_records*100, 2)
                    },
                    {
                        "identifier": "Unemployed Not Searching",
                        "number": unemployed_not_looking,
                        "total_count": employment_records,
                        "percentage": round(unemployed_not_looking/employment_records*100, 2)
                    },
                    {
                        "identifier": "Unemployed",
                        "number": unemployed,
                        "total_count": employment_records,
                        "percentage": round(unemployed/employment_records*100, 2)
                    },
                    {
                        "identifier": "Housed",
                        "number": housed,
                        "total_count": type_count,
                        "percentage": round(housed/type_count*100, 2)
                    },
                    {
                        "identifier": "Homeless",
                        "number": homeless,
                        "total_count": type_count,
                        "percentage": round(homeless/type_count*100, 2)
                    },
                ]
            }

class CountsByYear:
    def filterYear(year, records):
        recs = records.to_records()
        in_year = []
        for record in recs:
            if type(record[3]) == str:
                if int(record[3].split("/")[2]) == year:
                    in_year.append(record)
        in_year_records = pd.DataFrame.from_records(in_year)
        rename = in_year_records.rename(columns={0: "id", 1: "ConsumerID", 2: "Assessment", 3: "InterviewDate",
                                        4: "Gender", 5: "SexualIdentity", 6: "NightsHomeless", 7: "Housing", 8: "Employment"})
        return rename

    def logInfo(type, year, records):
        filtered_type_records = FormatCounts.filterInterviewType(
            type=type, records=records)
        type_records = filtered_type_records["records"]
        print(str(year) + " "+type.upper())
        year_records = CountsByYear.filterYear(year, type_records)
        # pprint(year_records)
        print("----------------------------------------------")
        if not year_records.empty:
            print("Total", FormatCounts.returnCount(year_records))
            pprint(FormatCounts.genderCount(type_records=year_records))
            pprint(FormatCounts.employmentCount(type_records=year_records))
            pprint(FormatCounts.housingCount(type_records=year_records))
        else:
            print("N/A")
        print("")

    def returnData(type, year, records):
        filtered_records = FormatCounts.filterInterviewType(
            type=type, records=records)
        print(str(year)+" "+type.upper())
        type_records = filtered_records["records"]
        year_records = CountsByYear.filterYear(year, type_records)
        if not year_records.empty:
            total_count = FormatCounts.returnCount(year_records)
            gender_count = FormatCounts.genderCount(type_records=year_records)
            female, male, heterosexual, non_heterosexual, male_non_heterosexual = itemgetter(
                "female", "male", "heterosexual", "non-heterosexual", "male-non-heterosexual")(gender_count)
            employment_count = FormatCounts.employmentCount(
                type_records=year_records)
            employment_records, disability, retired, full_time, part_time, employed, unemployed_searching, unemployed_not_looking, unemployed = itemgetter(
                "employment_records", "disability", "retired", "full_time", "part_time", "employed", "unemployed_searching", "unemployed_not_looking", "unemployed")(employment_count)
            housing_count = FormatCounts.housingCount(
                type_records=year_records)
            housed, homeless = itemgetter("housed", "homeless")(housing_count)
            if int(employment_records) == 0:
                return {
                    "title": str(year)+" "+" ".join(type.upper().split("_"))+" Records",
                    "data": [
                        {
                            "identifier": "Female",
                            "number": female,
                            "total_count": total_count,
                            "percentage": round(female/total_count*100, 2),
                        },
                        {
                            "identifier": "Male",
                            "number": male,
                            "total_count": total_count,
                            "percentage": round(male/total_count*100, 2),
                        },
                        {
                            "identifier": "Heterosexual",
                            "number": heterosexual,
                            "total_count": total_count,
                            "percentage": round(heterosexual/total_count*100, 2),
                        },
                        {
                            "identifier": "Non-Heterosexual",
                            "number": non_heterosexual,
                            "total_count": total_count,
                            "percentage": round(non_heterosexual/total_count*100, 2),
                        },
                        {
                            "identifier": "Male Non-Hetersexual",
                            "number": male_non_heterosexual,
                            "total_count": total_count,
                            "percentage": round(male_non_heterosexual/total_count*100, 2),
                        },
                        {
                            "identifier": "Employed Part Time",
                            "number": "MISSING DATA",
                            "total_count": "MISSING DATA",
                            "percentage": "MISSING DATA"
                        },
                        {
                            "identifier": "Employed Full Time",
                            "number": "MISSING DATA",
                            "total_count": "MISSING DATA",
                            "percentage": "MISSING DATA"
                        },
                        {
                            "identifier": "Employed",
                            "number": "MISSING DATA",
                            "total_count": "MISSING DATA",
                            "percentage": "MISSING DATA"
                        },
                        {
                            "identifier": "Receiving Disability",
                            "number": "MISSING DATA",
                            "total_count": "MISSING DATA",
                            "percentage": "MISSING DATA"
                        },
                        {
                            "identifier": "Retired",
                            "number": "MISSING DATA",
                            "total_count": "MISSING DATA",
                            "percentage": "MISSING DATA"
                        },
                        {
                            "identifier": "Unemployed Searching for Work",
                            "number": "MISSING DATA",
                            "total_count": "MISSING DATA",
                            "percentage": "MISSING DATA"
                        },
                        {
                            "identifier": "Unemployed Not Searching",
                            "number": "MISSING DATA",
                            "total_count": "MISSING DATA",
                            "percentage": "MISSING DATA"
                        },
                        {
                            "identifier": "Unemployed",
                            "number": "MISSING DATA",
                            "total_count": "MISSING DATA",
                            "percentage": "MISSING DATA"
                        },
                        {
                            "identifier": "Housed",
                            "number": housed,
                            "total_count": total_count,
                            "percentage": round(housed/total_count*100, 2)
                        },
                        {
                            "identifier": "Homeless",
                            "number": homeless,
                            "total_count": total_count,
                            "percentage": round(homeless/total_count*100, 2)
                        },
                    ]
                }
            else:
                return {
                    "title": str(year)+" "+" ".join(type.upper().split("_"))+" Records",
                    "data": [
                        {
                            "identifier": "Female",
                            "number": female,
                            "total_count": total_count,
                            "percentage": round(female/total_count*100, 2),
                        },
                        {
                            "identifier": "Male",
                            "number": male,
                            "total_count": total_count,
                            "percentage": round(male/total_count*100, 2),
                        },
                        {
                            "identifier": "Heterosexual",
                            "number": heterosexual,
                            "total_count": total_count,
                            "percentage": round(heterosexual/total_count*100, 2),
                        },
                        {
                            "identifier": "Non-Heterosexual",
                            "number": non_heterosexual,
                            "total_count": total_count,
                            "percentage": round(non_heterosexual/total_count*100, 2),
                        },
                        {
                            "identifier": "Male Non-Hetersexual",
                            "number": male_non_heterosexual,
                            "total_count": total_count,
                            "percentage": round(male_non_heterosexual/total_count*100, 2),
                        },
                        {
                            "identifier": "Employed Part Time",
                            "number": part_time,
                            "total_count": employment_records,
                            "percentage": round(part_time/employment_records*100, 2)
                        },
                        {
                            "identifier": "Employed Full Time",
                            "number": full_time,
                            "total_count": employment_records,
                            "percentage": round(full_time/employment_records*100, 2)
                        },
                        {
                            "identifier": "Employed",
                            "number": employed,
                            "total_count": employment_records,
                            "percentage": round(employed/employment_records*100, 2)
                        },
                        {
                            "identifier": "Receiving Disability",
                            "number": disability,
                            "total_count": employment_records,
                            "percentage": round(disability/employment_records*100, 2)
                        },
                        {
                            "identifier": "Retired",
                            "number": retired,
                            "total_count": employment_records,
                            "percentage": round(retired/employment_records*100, 2)
                        },
                        {
                            "identifier": "Unemployed Searching for Work",
                            "number": unemployed_searching,
                            "total_count": employment_records,
                            "percentage": round(unemployed_searching/employment_records*100, 2)
                        },
                        {
                            "identifier": "Unemployed Not Searching",
                            "number": unemployed_not_looking,
                            "total_count": employment_records,
                            "percentage": round(unemployed_not_looking/employment_records*100, 2)
                        },
                        {
                            "identifier": "Unemployed",
                            "number": unemployed,
                            "total_count": employment_records,
                            "percentage": round(unemployed/employment_records*100, 2)
                        },
                        {
                            "identifier": "Housed",
                            "number": housed,
                            "total_count": total_count,
                            "percentage": round(housed/total_count*100, 2)
                        },
                        {
                            "identifier": "Homeless",
                            "number": homeless,
                            "total_count": total_count,
                            "percentage": round(homeless/total_count*100, 2)
                        },
                    ]
                }
        else:
            return -1

def generateHTML(data):

    doc, tag, _, line = Doc().ttl()
    doc.asis("<!DOCTYPE html>")
    with tag("html"):
        with tag("head"):
            line("title", "NORA MOUD Data")
            doc.stag("link", href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css", rel="stylesheet",
                     integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD", crossOrigin="anonymous")
        with tag("body", klass="bg-dark text-white"):
            with tag("div", klass="container"):
                line("h1", "NORA MOUD Demographics", klass="text-center title my-5")
                for section in data:
                    title = section["title"]
                    record_data = section["data"]
                    with tag("div", klass="mb-5"):
                        line("h1", title)
                        with tag("table", klass="table table-striped table-hover bg-body text-body"):
                            with tag("thead"):
                                with tag("tr"):
                                    line("th", "Identifier")
                                    line("th", "Clients Identified")
                                    line("th", "Sample Population")
                                    line("th", "Percent")
                                with tag("tbody"):
                                    for record in record_data:
                                        identifier = record["identifier"]
                                        number = record["number"]
                                        total_count = record["total_count"]
                                        percentage = record["percentage"]
                                        with tag("tr"):
                                            line("th", identifier)
                                            line("td", str(number))
                                            line("td", str(total_count))
                                            line("td", percentage)
                        doc.stag("hr")
    sys.stdout = open("NORA_MOUD_DATA.html", "w")
    print(doc.getvalue())



# all_data = []
data = RetrieveRecords.getRecords()

# formatted_intakes = FormatCounts.returnData(type="intake", records=records)
# all_data.append(formatted_intakes)
# intake_2021 = CountsByYear.returnData(
#     type="intake", year=2021, records=records)
# if intake_2021 != -1:
#     all_data.append(intake_2021)
# intake_2022 = CountsByYear.returnData(
#     type="intake", year=2022, records=records)
# if intake_2022 != -1:
#     all_data.append(intake_2022)
# intake_2023 = CountsByYear.returnData(
#     type="intake", year=2023, records=records)
# if intake_2023 != -1:
#     all_data.append(intake_2023)
# pprint(formatted_intakes)

# formatted_followups = FormatCounts.returnData(type="followup", records=records)
# all_data.append(formatted_followups)
# followup_2021 = CountsByYear.returnData(
#     type="followup", year=2021, records=records)
# if followup_2021 != -1:
#     all_data.append(followup_2021)
# followup_2022 = CountsByYear.returnData(
#     type="followup", year=2022, records=records)
# if followup_2022 != -1:
#     all_data.append(followup_2022)
# followup_2023 = CountsByYear.returnData(
#     type="followup", year=2023, records=records)
# if followup_2023 != -1:
#     all_data.append(followup_2023)

# second_formatted_followups = FormatCounts.returnData(
#     type="second_followup", records=records)
# all_data.append(second_formatted_followups)
# second_2021_followups = CountsByYear.returnData(
#     type="second_followup", year=2021, records=records)
# if second_2021_followups != -1:
#     all_data.append(second_2021_followups)
# second_2022_followups = CountsByYear.returnData(
#     type="second_followup", year=2022, records=records)
# if second_2022_followups != -1:
#     all_data.append(second_2022_followups)
# second_2023_followups = CountsByYear.returnData(
#     type="second_followup", year=2023, records=records)
# if second_2023_followups != -1:
#     all_data.append(second_2023_followups)

# formatted_discharges = FormatCounts.returnData(type="discharge", records=records)
# all_data.append(formatted_discharges)
# discharge_2021 = CountsByYear.returnData(
#     type="discharge", year=2021, records=records)
# if discharge_2021 != -1:
#     all_data.append(discharge_2021)
# discharge_2022 = CountsByYear.returnData(
#     type="discharge", year=2022, records=records)
# if discharge_2022 != -1:
#     all_data.append(discharge_2022)
# discharge_2023 = CountsByYear.returnData(
#     type="discharge", year=2023, records=records)
# if discharge_2023 != -1:
#     all_data.append(discharge_2023)

# pprint(all_data)
# generateHTML(all_data)
