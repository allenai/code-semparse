# Leveraging Code to Improve In-context Learning for Semantic Parsing

Code for the paper [Leveraging Code to Improve In-context Learning for Semantic Parsing](https://arxiv.org/abs/2311.09519).

This repository will allow you to evaluate semantic parsing datasets using general-purpose code rather than domain-specific languages (DSLs), showing superior generalization, nearly closing the performance gap between i.i.d. splits and harder compositional splits.


## Running experiments 

1. First, install requirements:
```
pip install -r requirements.txt
```
2. Copy `env.example` to `.env` and fill in the value for the openai api key (unless vllm server is used)
```
cp env.example .env
```

3. The `run_experiment.py` file will evaluate the dataset of your choice given the selected prompt style and programming language, for example:

```
cd code_semparse
python run_experiment.py --dataset_name geo880 --prompt_lang python --prompt_method full_dd
```

------
The following arguments are available:
```
--dataset_name  # dataset to evaluate on: [geo880, overnight, smcalflow]
--overnight_domain  # when evaluating on overnight, the domain to be used (only socialnetwork has available programs)
--split_name  # the train/test split to be used. For geoquery avilable splits are [standard, template_1, tmcd_1, length], for overnight [iid, template/split_{0,1,2,3,4}], for smcalflow [iid, source_domain_with_target_num{0,8,16,32,64,128}]
--eval_set_name  # the set to be evaluated on, "valid" or "test"
--n_training_demonstrations  # number of in-context demonstrations to be used
--n_test_samples  # number of test samples to evaluate on
--model  # the openai model to be used. To use with open-source models, we ran vllm server and replaced the openai api url
--prompt_lang  # the programming language to be used for the prompt. For all datasets [python, javascript, scala], for geoquery also [funql], for overnight [dcs, dcs_simplified], for smcalflow [dataflow, simplified]
--prompt_method  # the prompting variation. full_dd for full domain description, no_dd for no domain description, list_of_operators for a list of operators, no_typing for full dd without typing
--icl_selection_method  # the method to select the in-context demonstrations. fixed_random for random, cover_atoms_oracle for an oracle selection of demonstrations based on targets
```