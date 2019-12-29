#! /usr/bin/env python3

import pygame, os, re
from scene_classes import Menu, Game, WinScreen


def main():
    pygame.init()

    # ensure we're in the right directory to load the levels
    if os.path.basename(os.getcwd()) != 'levels':
        if os.path.basename(os.getcwd()) == 'maze_game':
            os.chdir('levels')
        elif os.path.basename(os.getcwd()) == 'images':
            os.chdir('../levels')
        else:
            raise Exception('where are you??')

    # WinScreen() doesn't need any programmatic initialisation so we can
    # just start our scenes dictionary with an instance of it.
    scenes = {'win_screen': WinScreen()}
    
    # file_list has full filenames with extensions. levels_list will have
    # the filenames without the extensions
    files_list = os.listdir()
    levels_list = []

    # valid levels filenames are named like 0-00.lvl
    level_regexp = re.compile('(\d-\d{2})(\.lvl)')
        
    for filename in sorted(files_list):
        match = level_regexp.findall(filename)
        if match:
            try:
                level_name = match[0][0]
                fullname = level_name + match[0][1]
                levels_list.append(level_name)
                
                # the next stage could be done as:
                # scenes[level_name] = Game(fullname)
                # but the exception handling only works if they're
                # split up like this.
                scenes[level_name] = None
                new_level = Game(fullname)
                scenes[level_name] = new_level
                
            except BadLevelException as e:
                # if any levels fail validation, tell the user and
                # make sure that level isn't accessible in the game. This
                # validation will get built into the level editor so
                # eventually you shouldn't be able to get here
                print(e.what)
                del scenes[level_name]
                levels_list.remove(level_name)
    
    scenes['menu'] = Menu(sorted(levels_list))
    
    clock = pygame.time.Clock()

    scene = scenes['menu']
    
    while True:
        scene = scene.handle_all(clock, scenes)

        
if __name__ == '__main__':
    main()
