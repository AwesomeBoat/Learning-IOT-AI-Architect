# Algorithme secConverter
# DEBUT
#     Variable in_sec, out_sec, out_min, out_hour : Entier
#     Read(in_sec)
#     out_days = in_sec // 3600*24
#     out_hour = (in_sec - (out_days*3600*24)) // 3600
#     out_min = (in_sec - (out_days * 3600 * 24) - (out_hour*3600)) // 60
#     out_sec = (in_sec - (out_days * 3600 * 24) - (out_hour*3600) - (out_min*60))
#     Write(in_sec)
# FIN

in_secs = int(input("Enter the number of seconds to convert: : "))
out_days = in_secs // (3600*24)
out_hours = (in_secs - (out_days*3600*24)) // 3600
out_mins = (in_secs - (out_days * 3600 * 24) - (out_hours*3600)) // 60
out_secs = (in_secs - (out_days * 3600 * 24) - (out_hours*3600) - (out_mins*60))
print(f"{in_secs} seconds is equal to {out_days} days {out_hours} hours {out_mins} minutes and {out_secs}seconds")
