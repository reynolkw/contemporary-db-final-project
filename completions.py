from openai import OpenAI
import json

client = OpenAI()

def get_forecast_summary(forecasted_temp_f: int, factors: str):
  with open("system.txt", "r") as system:
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      response_format={ "type": "json_object" },
      messages=[
        {"role": "system", "content": f"{system.read()}"},
        {"role": "user", "content": f"Forecasted Temperature: {forecasted_temp_f} F, Unique Weather Descriptions: {factors}"}
      ]
  )

  return json.loads(completion.choices[0].message.content)

