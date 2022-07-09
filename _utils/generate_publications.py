import yaml

import bibtexparser


bibtex_files = {
    "en": "_bibliography/papers.bib",
    "ja": "_bibliography/papers_ja.bib"
}


myself = "Kento Nozawa"
ignore_paper_ids = {"KI2022arxiv", "KI2019"}

with open("./coauthors.yml") as f:
    coauthor_info = yaml.load(f, Loader=yaml.FullLoader)


def add_markdown_to_authors(authors):

    author_list = authors.split(" and ")
    for i, author in enumerate(author_list):
        # convert author name format
        author_elements = author.split(", ")
        author = author_elements[1] + " " + author_elements[0]

        if author in coauthor_info:
            author = f'[{author}]({coauthor_info[author]["url"]})'

        if author == myself:
            author = author.replace(myself, f"__{myself}__")

        author_list[i] = author

    if len(author_list) == 1:
        return author_list[0]
    elif len(author_list) == 2:
        return " and ".join(author_list)
    else:
        return ", ".join(author_list[:-1]) + " and " + author_list[-1]


# english
path = bibtex_files["en"]

selected_list = []
preprint_list = []

with open(path) as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

    sorted_entries = sorted(bib_database.entries, key=lambda x: -int(x["year"]))

    for entry in sorted_entries:
        if entry["ID"] in ignore_paper_ids:
            continue

        authors = add_markdown_to_authors(entry["author"])

        title = entry["title"][1:-1]

        line = f"1. {authors}. {title}. "

        # avenue
        if "booktitle" in entry:
            avenue = f'In _{entry["booktitle"]}_, '
        elif "journal" in entry:
            avenue = f'_{entry["journal"]}_'
        else:
            avenue = ""

        line += avenue

        # page, vol, num
        if "pages" in entry:
            pages = f'pages {entry["pages"]}, '
            line += pages
        # skip vol and num
        # if "volume" in entry:
        #     volume = entry["volume"]
        # if "number" in entry:
        #     number = entry["number"]

        year = entry["year"] + "."
        line += year

        # external links
        external_links = []

        # additional content
        # mainly they are on external platform such as youtue
        for material in ["paper", "video", "pdf", "slides", "code", "poster"]:
            if material in entry:
                link = f'[`{material}`]({entry[material]})'
                external_links.append(link)

        # arXiv
        if "arxiv" in entry:
            arxiv_url = f'https://arxiv.org/abs/{entry["arxiv"]}'
            arxiv_link = f'[`arXiv`]({arxiv_url})'
            external_links.append(arxiv_link)

        if external_links:
            line += " " + ", ".join(external_links) + "."

        # misc info
        if "footnote" in entry:
            line += '<label for="sn-1" class="sidenote-toggle sidenote-number"></label>' + '<input type="checkbox" id="sn-1" class="sidenote-toggle" />' + f'<span class="sidenote">{entry["footnote"]}</span>'

        if entry["ENTRYTYPE"] == "techreport":
            preprint_list.append(line)
        else:
            # exclude workshop
            if "Workshop" in line:
                continue
            selected_list.append(line)

with open("../_includes/publication.md", "w") as f:
    f.write("## Journal / Conference papers\n\n")
    f.write("\n".join(selected_list))
    f.write("\n")
    f.write("\n")

    f.write("## Pre-print\n\n")
    if len(preprint_list) > 0:
        f.write("\n".join(preprint_list))
    else:
        f.write(":(")
    f.write("\n")
