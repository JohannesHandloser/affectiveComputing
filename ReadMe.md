# Repository for Affective Computing Course at LMU Munich in WS 17/18

This Repository holds the Source-Code for the Server for the Affective Computing Course at LMU Munich in WS 17/18. Goal was to build an AI to 
make decisions about music playlists depending on your current physiological state. The physiological data was tracked via a 
Microsoft Band and an iOS App. The App also connects to spotify to get the songs with their metadata.
Data from the iOS Device was putted up on a firebase DB. On the Server data was preprocessed and classified by different classifiers.
A Pipeline was build to run different settings automatically and in parallel.

 - Branch **master** holds the finished pipeline for project delivery
 - Branch **rl_server** holds a Reinforcement Learning approach for a first Draft
 - **other branches** hold different tryouts for classification and pipeline approaches
 
The Code for the iOS-Device is on a different GitLab Repository and can be viewed separately 
