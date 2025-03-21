from argparse import ArgumentParser

def main():
    try:
        import yaml
    except:
        print("Install PyYaml") 
        exit(1)

    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        required=True,
        type=str,
        help="Yaml document to parse"
    )

    parser.add_argument(
        "-o",
        required=True,
        type=str,
        help="Output"
    )

    args = parser.parse_args()

    def parse_date(date):
        parsed_date = ""
        if date["month"] or date["year"]:
            parsed_date = "%s %s" % (
                date["month"] if date["month"] else "",
                date["year"] if date["year"] else ""
            )
            parsed_date.strip()
        return parsed_date


    def unpack_experience(experience):
        start_date = experience["start-date"]
        end_date = experience["end-date"]
        parsed_start_date = parse_date(start_date)
        parsed_end_date = parse_date(end_date)
        job_title = ' #job("{}", "{}", "{}", "{}", "{}")'.format(
                        experience["job-position"],
                        experience["company"],
                        parsed_start_date,
                        parsed_end_date,
                        ", ".join([experience["location"]["city"], experience["location"]["country"]]) 
        )
        description = "],[ ".join([job_function["description"] for job_function in experience["job-functions"]])
        if not description == "":
            description = "\\\n#list([" + description + "])"
        return job_title + description

    def unpack_experiences(experiences):
        return "\n".join([unpack_experience(experience) for experience in experiences])

    def unpack_education(education):
        start_date = education["start-date"]
        end_date = education["end-date"]
        parsed_start_date = parse_date(start_date)
        parsed_end_date = parse_date(end_date)
        education_title = '#education("{}", "{}", "{}", "{}", "{}", "{}")'.format(
                        education["type"],
                        education["study-line"],
                        education["institution"],
                        parsed_start_date,
                        parsed_end_date,
                        ", ".join([education["location"]["city"], education["location"]["country"]]) 
                    )
        description = "], [".join([remark for remark in education["remarks"]])
        if not description == "":
            description = "\\\n#list( [" + description + "])"
        return education_title + description

    def unpack_educations(educations):
        return "\\\n".join([unpack_education(education) for education in educations])

    template = """
#set page(
      paper: "a4",
    )
#set par(justify: true)

#let job(position, where, date_start, date_end, location) = {
      if date_end == "" { date_end = "Present" }
      [*#position, #where* | #text(10pt)[From #date_start - #date_end, #location]]
    }

#let education(type, title, institution, date_start, date_end, location) = {
      if date_end == "" { date_end = "Present" }
      [*#type #title*, #institution | #text(10pt)[From #date_start - #date_end, #location]]
    }

    = %(name)s
    _%(motd)s_\\
    %(contact)s\\
    %(links)s

    = Experiences
    %(experiences)s

    = Education
    %(education)s

    = Skills
    *Technical*: %(technical)s\\
    *Programming*: %(programming)s\\
    *Soft Skills*: %(soft)s

    = Honors
    %(honors)s
    """

    values = {}

    with open(args.i, "r") as f:
        yml_raw = yaml.load(f, Loader=yaml.Loader)

    values["name"] = yml_raw["name"]
    values["motd"] = yml_raw["motd"]
    values["contact"] = ", ".join(["{}: {}".format(itm["name"], itm["value"]) for itm in yml_raw["contacts"]])
    values["links"] = ", ".join(["{}: {}".format(itm["name"], itm["value"]) for itm in yml_raw["links"]])
    values["experiences"] = unpack_experiences(yml_raw["experiences"])
    values["education"] =  unpack_educations(yml_raw["education"])
    values["technical"] = ", ".join([" ".join(skill.split("_")).title() for skill in yml_raw["skills"]["technical"]])
    values["programming"] = ", ".join([" ".join(skill.split("_")).title() for skill in yml_raw["skills"]["programming_languages"]])
    values["soft"] = ", ".join([" ".join(skill.split("_")).title() for skill in yml_raw["skills"]["soft"]])
    values["honors"] = ", ".join(yml_raw["honors"])

    with open(args.o + ".typ", "w") as f:
        complete_text = template % values
        complete_text = complete_text.replace("@", "\\@")
        f.writelines(complete_text)

if __name__ == "__main__": main()
