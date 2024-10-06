import pets

database_path = "pets.db"

pets.update_database(
    lost_url="https://petharbor.com/results.asp?searchtype=LOST&start=4&friends=1&samaritans=1&nosuccess=0&rows=10&imght=120&imgres=detail&tWidth=200&view=sysadm.v_sncr&nobreedreq=1&bgcolor=ffffff&text=000000&fontface=arial&fontsize=10&col_hdr_bg=c0c0c0&SBG=c0c0c0&miles=20&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_CAT&PAGE=1",
    adoptable_url="https://petharbor.com/results.asp?searchtype=ADOPT&friends=1&samaritans=1&nosuccess=0&rows=25&imght=120&imgres=thumb&view=sysadm.v_sncr&bgcolor=white&text=black&link=blue&alink=purple&vlink=purple&fontface=arial&fontsize=10&col_hdr_bg=silver&col_hdr_fg=black&col_bg=white&col_fg=black&SBG=silver&miles=200&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_CAT&PAGE=1",
    database_path=database_path,
    table="cats"
)

pets.update_database(
    lost_url="https://petharbor.com/results.asp?searchtype=LOST&start=4&friends=1&samaritans=1&nosuccess=0&rows=10&imght=120&imgres=detail&tWidth=200&view=sysadm.v_sncr&nobreedreq=1&bgcolor=ffffff&text=000000&fontface=arial&fontsize=10&col_hdr_bg=c0c0c0&SBG=c0c0c0&miles=20&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_DOG&PAGE=1",
    adoptable_url="https://petharbor.com/results.asp?searchtype=ADOPT&friends=1&samaritans=1&nosuccess=0&rows=25&imght=120&imgres=thumb&view=sysadm.v_sncr&bgcolor=white&text=black&link=blue&alink=purple&vlink=purple&fontface=arial&fontsize=10&col_hdr_bg=silver&col_hdr_fg=black&col_bg=white&col_fg=black&SBG=silver&miles=200&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_DOG&PAGE=1",
    database_path=database_path,
    table="dogs"
)

pets.update_database(
    lost_url="https://petharbor.com/results.asp?searchtype=LOST&start=4&friends=1&samaritans=1&nosuccess=0&rows=10&imght=120&imgres=detail&tWidth=200&view=sysadm.v_sncr&nobreedreq=1&bgcolor=ffffff&text=000000&fontface=arial&fontsize=10&col_hdr_bg=c0c0c0&SBG=c0c0c0&miles=20&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_OO&PAGE=1",
    adoptable_url="https://petharbor.com/results.asp?searchtype=ADOPT&friends=1&samaritans=1&nosuccess=0&rows=25&imght=120&imgres=thumb&view=sysadm.v_sncr&bgcolor=white&text=black&link=blue&alink=purple&vlink=purple&fontface=arial&fontsize=10&col_hdr_bg=silver&col_hdr_fg=black&col_bg=white&col_fg=black&SBG=silver&miles=200&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_OO&PAGE=1",
    database_path=database_path,
    table="others"
)
