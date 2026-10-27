@echo off
rem Range les originaux lourds des images hors du dossier game (ils ne sont pas livres avec le jeu).
rem Rien n est supprime : tout est deplace dans assets_sources
cd /d "%~dp0"
if exist "game\images\backgrounds\bg_attic.png" (
  if not exist "assets_sources\backgrounds" mkdir "assets_sources\backgrounds"
  move /Y "game\images\backgrounds\bg_attic.png" "assets_sources\backgrounds\bg_attic.png" >nul
)
if exist "game\images\backgrounds\bg_cellar.png" (
  if not exist "assets_sources\backgrounds" mkdir "assets_sources\backgrounds"
  move /Y "game\images\backgrounds\bg_cellar.png" "assets_sources\backgrounds\bg_cellar.png" >nul
)
if exist "game\images\backgrounds\bg_corridor_01.png" (
  if not exist "assets_sources\backgrounds" mkdir "assets_sources\backgrounds"
  move /Y "game\images\backgrounds\bg_corridor_01.png" "assets_sources\backgrounds\bg_corridor_01.png" >nul
)
if exist "game\images\backgrounds\bg_corridor_02.png" (
  if not exist "assets_sources\backgrounds" mkdir "assets_sources\backgrounds"
  move /Y "game\images\backgrounds\bg_corridor_02.png" "assets_sources\backgrounds\bg_corridor_02.png" >nul
)
if exist "game\images\backgrounds\bg_door_generic.png" (
  if not exist "assets_sources\backgrounds" mkdir "assets_sources\backgrounds"
  move /Y "game\images\backgrounds\bg_door_generic.png" "assets_sources\backgrounds\bg_door_generic.png" >nul
)
if exist "game\images\backgrounds\bg_entrance_hall.png" (
  if not exist "assets_sources\backgrounds" mkdir "assets_sources\backgrounds"
  move /Y "game\images\backgrounds\bg_entrance_hall.png" "assets_sources\backgrounds\bg_entrance_hall.png" >nul
)
if exist "game\images\backgrounds\bg_exterior_forest.png" (
  if not exist "assets_sources\backgrounds" mkdir "assets_sources\backgrounds"
  move /Y "game\images\backgrounds\bg_exterior_forest.png" "assets_sources\backgrounds\bg_exterior_forest.png" >nul
)
if exist "game\images\backgrounds\bg_gameover.png" (
  if not exist "assets_sources\backgrounds" mkdir "assets_sources\backgrounds"
  move /Y "game\images\backgrounds\bg_gameover.png" "assets_sources\backgrounds\bg_gameover.png" >nul
)
if exist "game\images\backgrounds\bg_library.png" (
  if not exist "assets_sources\backgrounds" mkdir "assets_sources\backgrounds"
  move /Y "game\images\backgrounds\bg_library.png" "assets_sources\backgrounds\bg_library.png" >nul
)
if exist "game\images\backgrounds\bg_manor_facade.png" (
  if not exist "assets_sources\backgrounds" mkdir "assets_sources\backgrounds"
  move /Y "game\images\backgrounds\bg_manor_facade.png" "assets_sources\backgrounds\bg_manor_facade.png" >nul
)
if exist "game\images\backgrounds\bg_secret_room.png" (
  if not exist "assets_sources\backgrounds" mkdir "assets_sources\backgrounds"
  move /Y "game\images\backgrounds\bg_secret_room.png" "assets_sources\backgrounds\bg_secret_room.png" >nul
)
if exist "game\images\backgrounds\bg_stairs.png" (
  if not exist "assets_sources\backgrounds" mkdir "assets_sources\backgrounds"
  move /Y "game\images\backgrounds\bg_stairs.png" "assets_sources\backgrounds\bg_stairs.png" >nul
)
if exist "game\images\backgrounds\bg_title.png" (
  if not exist "assets_sources\backgrounds" mkdir "assets_sources\backgrounds"
  move /Y "game\images\backgrounds\bg_title.png" "assets_sources\backgrounds\bg_title.png" >nul
)
if exist "game\images\backgrounds\bg_victory.png" (
  if not exist "assets_sources\backgrounds" mkdir "assets_sources\backgrounds"
  move /Y "game\images\backgrounds\bg_victory.png" "assets_sources\backgrounds\bg_victory.png" >nul
)
if exist "game\images\fx\fx_candle_flicker_01.png" (
  if not exist "assets_sources\fx" mkdir "assets_sources\fx"
  move /Y "game\images\fx\fx_candle_flicker_01.png" "assets_sources\fx\fx_candle_flicker_01.png" >nul
)
if exist "game\images\fx\fx_candle_flicker_02.png" (
  if not exist "assets_sources\fx" mkdir "assets_sources\fx"
  move /Y "game\images\fx\fx_candle_flicker_02.png" "assets_sources\fx\fx_candle_flicker_02.png" >nul
)
if exist "game\images\fx\fx_candle_flicker_03.png" (
  if not exist "assets_sources\fx" mkdir "assets_sources\fx"
  move /Y "game\images\fx\fx_candle_flicker_03.png" "assets_sources\fx\fx_candle_flicker_03.png" >nul
)
if exist "game\images\fx\fx_fog_overlay.png" (
  if not exist "assets_sources\fx" mkdir "assets_sources\fx"
  move /Y "game\images\fx\fx_fog_overlay.png" "assets_sources\fx\fx_fog_overlay.png" >nul
)
if exist "game\images\fx\fx_ink_transition.png" (
  if not exist "assets_sources\fx" mkdir "assets_sources\fx"
  move /Y "game\images\fx\fx_ink_transition.png" "assets_sources\fx\fx_ink_transition.png" >nul
)
if exist "game\images\fx\fx_torn_paper_frame.png" (
  if not exist "assets_sources\fx" mkdir "assets_sources\fx"
  move /Y "game\images\fx\fx_torn_paper_frame.png" "assets_sources\fx\fx_torn_paper_frame.png" >nul
)
if exist "game\images\map\map_frame_puzzle.png" (
  if not exist "assets_sources\map" mkdir "assets_sources\map"
  move /Y "game\images\map\map_frame_puzzle.png" "assets_sources\map\map_frame_puzzle.png" >nul
)
if exist "game\images\map\map_full.png" (
  if not exist "assets_sources\map" mkdir "assets_sources\map"
  move /Y "game\images\map\map_full.png" "assets_sources\map\map_full.png" >nul
)
if exist "game\images\map\map_piece_01.png" (
  if not exist "assets_sources\map" mkdir "assets_sources\map"
  move /Y "game\images\map\map_piece_01.png" "assets_sources\map\map_piece_01.png" >nul
)
if exist "game\images\map\map_piece_02.png" (
  if not exist "assets_sources\map" mkdir "assets_sources\map"
  move /Y "game\images\map\map_piece_02.png" "assets_sources\map\map_piece_02.png" >nul
)
if exist "game\images\map\map_piece_03.png" (
  if not exist "assets_sources\map" mkdir "assets_sources\map"
  move /Y "game\images\map\map_piece_03.png" "assets_sources\map\map_piece_03.png" >nul
)
if exist "game\images\map\map_piece_04.png" (
  if not exist "assets_sources\map" mkdir "assets_sources\map"
  move /Y "game\images\map\map_piece_04.png" "assets_sources\map\map_piece_04.png" >nul
)
if exist "game\images\map\map_piece_05.png" (
  if not exist "assets_sources\map" mkdir "assets_sources\map"
  move /Y "game\images\map\map_piece_05.png" "assets_sources\map\map_piece_05.png" >nul
)
if exist "game\images\map\map_piece_06.png" (
  if not exist "assets_sources\map" mkdir "assets_sources\map"
  move /Y "game\images\map\map_piece_06.png" "assets_sources\map\map_piece_06.png" >nul
)
if exist "game\images\map\map_piece_07.png" (
  if not exist "assets_sources\map" mkdir "assets_sources\map"
  move /Y "game\images\map\map_piece_07.png" "assets_sources\map\map_piece_07.png" >nul
)
if exist "game\images\map\map_piece_08.png" (
  if not exist "assets_sources\map" mkdir "assets_sources\map"
  move /Y "game\images\map\map_piece_08.png" "assets_sources\map\map_piece_08.png" >nul
)
if exist "game\images\map\piece_01.png" (
  if not exist "assets_sources\map" mkdir "assets_sources\map"
  move /Y "game\images\map\piece_01.png" "assets_sources\map\piece_01.png" >nul
)
if exist "game\images\map\piece_02.png" (
  if not exist "assets_sources\map" mkdir "assets_sources\map"
  move /Y "game\images\map\piece_02.png" "assets_sources\map\piece_02.png" >nul
)
if exist "game\images\map\piece_03.png" (
  if not exist "assets_sources\map" mkdir "assets_sources\map"
  move /Y "game\images\map\piece_03.png" "assets_sources\map\piece_03.png" >nul
)
if exist "game\images\map\piece_04.png" (
  if not exist "assets_sources\map" mkdir "assets_sources\map"
  move /Y "game\images\map\piece_04.png" "assets_sources\map\piece_04.png" >nul
)
if exist "game\images\riddles\illus_riddle_book.png" (
  if not exist "assets_sources\riddles" mkdir "assets_sources\riddles"
  move /Y "game\images\riddles\illus_riddle_book.png" "assets_sources\riddles\illus_riddle_book.png" >nul
)
if exist "game\images\riddles\illus_riddle_clock.png" (
  if not exist "assets_sources\riddles" mkdir "assets_sources\riddles"
  move /Y "game\images\riddles\illus_riddle_clock.png" "assets_sources\riddles\illus_riddle_clock.png" >nul
)
if exist "game\images\riddles\illus_riddle_lock.png" (
  if not exist "assets_sources\riddles" mkdir "assets_sources\riddles"
  move /Y "game\images\riddles\illus_riddle_lock.png" "assets_sources\riddles\illus_riddle_lock.png" >nul
)
if exist "game\images\riddles\illus_riddle_mirror.png" (
  if not exist "assets_sources\riddles" mkdir "assets_sources\riddles"
  move /Y "game\images\riddles\illus_riddle_mirror.png" "assets_sources\riddles\illus_riddle_mirror.png" >nul
)
if exist "game\images\riddles\illus_riddle_portrait.png" (
  if not exist "assets_sources\riddles" mkdir "assets_sources\riddles"
  move /Y "game\images\riddles\illus_riddle_portrait.png" "assets_sources\riddles\illus_riddle_portrait.png" >nul
)
if exist "game\images\ui\bg_manor_facade.png" (
  if not exist "assets_sources\ui" mkdir "assets_sources\ui"
  move /Y "game\images\ui\bg_manor_facade.png" "assets_sources\ui\bg_manor_facade.png" >nul
)
if exist "game\images\ui\bg_title.png" (
  if not exist "assets_sources\ui" mkdir "assets_sources\ui"
  move /Y "game\images\ui\bg_title.png" "assets_sources\ui\bg_title.png" >nul
)
if exist "game\images\ui\btn_load.png" (
  if not exist "assets_sources\ui" mkdir "assets_sources\ui"
  move /Y "game\images\ui\btn_load.png" "assets_sources\ui\btn_load.png" >nul
)
if exist "game\images\ui\btn_load_hover.png" (
  if not exist "assets_sources\ui" mkdir "assets_sources\ui"
  move /Y "game\images\ui\btn_load_hover.png" "assets_sources\ui\btn_load_hover.png" >nul
)
if exist "game\images\ui\btn_quit.png" (
  if not exist "assets_sources\ui" mkdir "assets_sources\ui"
  move /Y "game\images\ui\btn_quit.png" "assets_sources\ui\btn_quit.png" >nul
)
if exist "game\images\ui\btn_quit_hover.png" (
  if not exist "assets_sources\ui" mkdir "assets_sources\ui"
  move /Y "game\images\ui\btn_quit_hover.png" "assets_sources\ui\btn_quit_hover.png" >nul
)
if exist "game\images\ui\btn_start.png" (
  if not exist "assets_sources\ui" mkdir "assets_sources\ui"
  move /Y "game\images\ui\btn_start.png" "assets_sources\ui\btn_start.png" >nul
)
if exist "game\images\ui\btn_start_hover.png" (
  if not exist "assets_sources\ui" mkdir "assets_sources\ui"
  move /Y "game\images\ui\btn_start_hover.png" "assets_sources\ui\btn_start_hover.png" >nul
)
if exist "game\images\ui\btn_start_v2.png" (
  if not exist "assets_sources\ui" mkdir "assets_sources\ui"
  move /Y "game\images\ui\btn_start_v2.png" "assets_sources\ui\btn_start_v2.png" >nul
)
if exist "game\images\ui\cursor.png" (
  if not exist "assets_sources\ui" mkdir "assets_sources\ui"
  move /Y "game\images\ui\cursor.png" "assets_sources\ui\cursor.png" >nul
)
if exist "game\images\ui\frame_dialogue.png" (
  if not exist "assets_sources\ui" mkdir "assets_sources\ui"
  move /Y "game\images\ui\frame_dialogue.png" "assets_sources\ui\frame_dialogue.png" >nul
)
if exist "game\images\ui\frame_ui_generic.png" (
  if not exist "assets_sources\ui" mkdir "assets_sources\ui"
  move /Y "game\images\ui\frame_ui_generic.png" "assets_sources\ui\frame_ui_generic.png" >nul
)
if exist "game\images\ui\icon_map_piece.png" (
  if not exist "assets_sources\ui" mkdir "assets_sources\ui"
  move /Y "game\images\ui\icon_map_piece.png" "assets_sources\ui\icon_map_piece.png" >nul
)
if exist "game\images\ui\icon_score.png" (
  if not exist "assets_sources\ui" mkdir "assets_sources\ui"
  move /Y "game\images\ui\icon_score.png" "assets_sources\ui\icon_score.png" >nul
)
if exist "game\images\ui\logo_title.png" (
  if not exist "assets_sources\ui" mkdir "assets_sources\ui"
  move /Y "game\images\ui\logo_title.png" "assets_sources\ui\logo_title.png" >nul
)
echo Images rangees dans assets_sources
pause
