import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("system_logs.csv")
df.plot(x="time", y=["cpu", "memory", "disk"], figsize=(10,6))
plt.title("System Resource Usage")
plt.ylabel("Percent (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
