from SheetCode import Sheet
import UTest

sheet = Sheet("FCT", __file__)

sheet.Name = "Buttons and lights"
sheet.Version = "1A"
sheet.Description = ["This test sheets covers the buttons and lights of all colors",
                        "We will test each button and check that the expected lights are lit on"]

sheet.StartConditions = ["No button is pressed",
                         "No light is lit on"]

canLogFilename = UTest.StartCanLog(__file__)

# *********************************
sheet.Case("Yellow light is managed")

sheet.Action("Press and maintain the yellow button")
UTest.SetVariable("YELLOW_BUTTON", True)

sheet.ExpectedResult("The yellow lights turns on and remains on",
                        requirements = ["[SIMPLE_REQ_1]"],
                        parameters = ["parameters/yellow_light_enabled"])

yellowLightState = UTest.GetVariable("YELLOW_LIGHT")
result = yellowLightState == True
sheet.Result(result, f"The state of Yellow light is {yellowLightState}")

sheet.ExpectedResult("The red light remains off",
                        requirements = ["[SIMPLE_REQ_2]"])

redLightState = UTest.GetVariable("RED_LIGHT")
result = redLightState == False
sheet.Result(result, f"The state of Red light is {result}")

sheet.Action("Release the yellow button")
UTest.SetVariable("YELLOW_BUTTON", False)

sheet.ExpectedResult("The yellow light turns off")
yellowLightState = UTest.GetVariable("YELLOW_LIGHT")
result = yellowLightState == False
sheet.Result(result, f"The state of Yellow light is {result}")

# *********************************
sheet.Case("Red light is not managed")

sheet.Action("Press and maintain the red button")

UTest.SetVariable("RED_BUTTON", True)

sheet.ExpectedResult("The red lights turns DOES NOT turn on",
                        requirements = ["[SIMPLE_REQ_3]"],
                        parameters = ["parameters/red_light_enabled"])

redLightState = UTest.GetVariable("RED_LIGHT")
result = redLightState == False
sheet.Result(result, f"The state of Red light is {redLightState}")

sheet.Action("Release the red button")
UTest.SetVariable("RED_BUTTON", False)

sheet.ExpectedResult("The red light remains off")

redLightState = UTest.GetVariable("RED_LIGHT")
result = redLightState == False
sheet.Result(result, f"The state of Red light is {redLightState}")

# *********************************

UTest.StopCanLog()

sheet.Logs.append(sheet.Log("Canapé", canLogFilename))

sheet.Save(checkRequirementsTraceability = True, checkParametersTraceability = True)