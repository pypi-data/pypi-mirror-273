
# MOdel Test Harness (Moth)

Simple way to interrogate your AI model from a separate testing application

# Quickstart

`moth server <folder path>`

`moth client`

# Client

Simple classification model client.
``` python
from moth import Moth
from moth.message import ImagePromptMsg, ClassificationResultMsg, HandshakeTaskTypes

moth = Moth("my-ai", task_type=HandshakeTaskTypes.CLASSIFICATION)

@moth.prompt
def on_prompt(prompt: ImagePromptMsg):
    # TODO: Do smart AI here
    return ClassificationResultMsg(prompt_id=prompt.id, class_name="cat") # Most pictures are cat pictures 

moth.run()
```

ClassificationResultMsg can optionally include a confidence value

``` python
ClassificationResultMsg(prompt_id=prompt.id, class_name="cat", confidence=0.9)
```

Simple object detection model client.
``` python
from moth import Moth
from moth.message import (
    ImagePromptMsg,
    ObjectDetectionResultMsg,
    ObjectDetectionResult,
    HandshakeTaskTypes,
)

moth = Moth("my-ai", task_type=HandshakeTaskTypes.OBJECT_DETECTION)


@moth.prompt
def on_prompt(prompt: ImagePromptMsg):
    # TODO: Do smart AI here
    # Make a list of ObjectDetectionResults
    results = []
    results.append(
        ObjectDetectionResult(
            0,
            0,
            50,
            50,
            class_name="cat",
            class_index=0,
            confidence=0.9,  # Optional confidence
        )
    )
    results.append(
        ObjectDetectionResult(
            10,
            10,
            50,
            35,
            class_name="dog",
            class_index=1,
            confidence=0.1,  # Optional confidence
        )
    )
    return ObjectDetectionResultMsg(
        prompt_id=prompt.id, object_detection_results=results
    )


moth.run()

```

Simple segmentation model client.
``` python
from moth import Moth
from moth.message import (
    ImagePromptMsg,
    SegmentationResultMsg,
    SegmentationResult,
    HandshakeTaskTypes,
)

moth = Moth("my-ai", task_type=HandshakeTaskTypes.SEGMENTATION)


@moth.prompt
def on_prompt(prompt: ImagePromptMsg):
    # TODO: Do smart AI here
    # Make a list of ObjectDetectionResults
    results = []
    results.append(
        SegmentationResult(
            [0, 0, 50, 50, 20, 20, 0, 0],  # The predicted polygon
            class_name="cat",
            class_index=0,
            confidence=0.9,  # Optional confidence
        )
    )
    results.append(
        SegmentationResult(
            [0, 0, 50, 50, 13, 20, 0, 0],  # The predicted polygon
            class_name="dog",
            class_index=1,
            confidence=0.1,  # Optional confidence
        )
    )
    return SegmentationResultMsg(prompt_id=prompt.id, results=results)


moth.run()
```

You can also define a set of client output classes that get sent to the server. We recommend you do this.
``` python
moth = Moth("my-ai", task_type=HandshakeTaskTypes.CLASSIFICATION, output_classes=["cat", "dog"])
```

# Server

Simple server.
``` python
from moth.server import Server
from moth.message import HandshakeMsg

class ModelDriverImpl(ModelDriver):
    # TODO: Implement your model driver here
    pass

server = Server(7171)

@server.driver_factory
def handle_handshake(handshake: HandshakeMsg) -> ModelDriver
    return ModelDriverImpl()
```

You can also subscribe to track changes to the current list of connected models.
``` python
from moth.server import Model

@server.on_model_change
def handle_model_change(model_list: List[Model]):
    print(f"Connected models: {model_list}")
```
