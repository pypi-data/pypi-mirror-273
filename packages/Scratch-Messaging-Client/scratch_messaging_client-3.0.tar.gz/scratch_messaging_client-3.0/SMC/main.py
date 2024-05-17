def SMC():
    import os


    game = input("Please enter the scratch id: ")
    text = input("Please enter text: ")

    import scratchattach as scratch3

    session = scratch3.login("very-cool-dude1", "usethispassword")
    project = session.connect_project(game)

    project.post_comment(text)
