import torch

class ModelProcess(object):
    def __init__(self) -> None:
        pass

    #key_replace_list = [(str, str),(str, str),(str, str), ...]
    def merge_model(self, model, path_src, path_merged, key_replace_list=None):
        checkpoint = torch.load(path_src)
        checkpoint_dict = dict(checkpoint.items())
        for mitemk, mitemv in torch.load(path_merged).items():
            if mitemk.split(".")[0] == "inst_head":
                mitemk = mitemk.replace("inst_head", "instance")
                checkpoint_dict.update({mitemk: mitemv})
            elif mitemk.split(".")[0] == "mask_head":
                mitemk = mitemk.replace("mask_head", "mask")
                checkpoint_dict.update({mitemk: mitemv})
        # for k ,v in checkpoint_dict.items():
        #     print(k)
        # print(checkpoint.items().append())
        model.load_state_dict(
            {k.replace('module.', ''): v for k, v in checkpoint_dict.items()})
        pass

    def show_keys(self, model):
        for key, v in model.cpu().state_dict().items():
            print(key)
    
    def auto_adapt(self, model, weight_path, strict=True): 
        new_weights = None
        new_weights = ModelProcess.auto_remove_items(model, weight_path, strict)
        new_weights = ModelProcess.auto_add_items(model, weight_path, strict)
        return new_weights

    @staticmethod
    def auto_remove_items(model, weight_path, strict=True):
        pretrained_weights = torch.load(weight_path, map_location=torch.device('cpu'))
        if len(pretrained_weights.keys()) == 1:
            pretrained_weights = pretrained_weights[list(pretrained_weights.keys())[0]]
        model.cpu()
        model_state_dict = model.state_dict()
        print(len(model_state_dict.keys()))
        print(len(pretrained_weights.keys()))
        for key, value in pretrained_weights.items():
            if key not in model_state_dict:
                print("Del key: {}", key)
            else:
                if pretrained_weights[key].shape == value.shape:
                    model_state_dict[key] = value
                else:
                    pass
                print("Skipping", key, "as it already exists")
        model.load_state_dict(model_state_dict, strict)
        return model

    @staticmethod
    def auto_add_items(model, weight_path, strict=True):
        pretrained_weights = torch.load(weight_path, map_location=torch.device('cpu'))
        if len(pretrained_weights.keys()) == 1:
            pretrained_weights = pretrained_weights[list(pretrained_weights.keys())[0]]
        model.cpu()
        model_state_dict = model.state_dict()
        print(len(model_state_dict.keys()))
        print(len(pretrained_weights.keys()))
        for key, value in model_state_dict.items():
            if key not in pretrained_weights:
                # value = random.uniform(0, 1)
                print("Add Key: {}".format(key))
                pretrained_weights[key] = value
            else:
                if pretrained_weights[key].shape == value.shape:
                # pass
                    print("Skipping", key, "as it already exists")
                else:
                    pretrained_weights[key] = value

        # print(model_state_dict)
        model.load_state_dict(pretrained_weights, strict)
        return model

    def remove_layer(self, model_loaded, layer_name, strict=True):
        model_state_dict = model_loaded.state_dict()
        if layer_name in model_state_dict.keys():
            del model_state_dict[layer_name]
        model_loaded.load_state_dict(model_state_dict, strict)
        return model_loaded
    