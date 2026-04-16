To run both the successful SGI script and the failing SGI script
just open the terminal on the proper cd and run the command "python gob_simple.py" or "python gob_sgi_fail.py"
depending on which one you want to run.

The successful SGI will identify the goal with the highest remaining value each step,
then use the most effective action to achieve that goal. It will happen
until both goals reach 0


A small disclaimer that the gob_sgi_fail.py works as an infinite loop between both goals, so be ready to 
terminate the terminal process