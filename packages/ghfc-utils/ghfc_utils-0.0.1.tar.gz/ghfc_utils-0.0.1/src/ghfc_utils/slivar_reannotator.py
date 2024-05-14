def reannotate(args):
    import yaml
    import pandas as pd
    import pkg_resources
    import pyranges as pr

    # reading the configuraiton yaml file
    config = yaml.safe_load(open(args.configuration))
    chunk_nb=0
    with pd.read_csv(args.slivar, sep='\t', dtype="string", chunksize=args.chunksize) as reader:
        for df in reader:
            print('chunk number:', chunk_nb)
            chunk_nb+=1

            # separating transcript for each variants
            df[config['slivar-field-name']] = df[config['slivar-field-name']].str.split(';')
            df = df.explode(config['slivar-field-name'])
            print('making a total of', len(df), 'transcripts impacted')

            # splitting the slivar transcript line, be careful, changing depending on slivar options, parameters in the config file are important
            df[config['slivar-field-decomposed']] = df[config['slivar-field-name']].str.split('/', expand=True)
            # TEMP drop config['slivar-field-name']
            df.drop(['gene', 'highest_impact', config['slivar-field-name']], axis=1, inplace=True)

            # filtering based on ENSG
            if 'geneset-file' in config:
                geneset = list(pd.read_csv(config['geneset-file'], sep='\t', names=['name'])['name'])
                df = df[df['ENSG'].isin(geneset)]
                print('after geneset filtering:', len(df), 'transcripts impacted')

            # importing impacts configuration
            yaml_impacts = yaml.safe_load(open(pkg_resources.resource_filename('ghfc_utils', 'resources/impacts.yaml')))
            impact_categories = list(yaml_impacts.keys())
            dict_rev_impacts = {}
            for k,v in yaml_impacts.items():
                for x in v:
                    dict_rev_impacts[x] = str(k)
                    dict_rev_impacts[x+"_variant"] = str(k)

            # filtering based on impacts
            list_impacts = config['impact-filter'] + [i+"_variant" for i in config['impact-filter']]
            for c in config['impact-categories-filter']:
                list_impacts = list_impacts + [i for i in yaml_impacts[c]] + [i+"_variant" for i in yaml_impacts[c]]
            list_impacts = list(set(list_impacts))
            df = df[df['impact'].isin(list_impacts)]
            print('after impact filtering:', len(df), 'transcripts impacted')

            # filters specific to missenses
            if 'missense' in list_impacts:
                if 'missense-filter' in config:
                    df[config['missense-filter']['mpc']['field']] = pd.to_numeric(df[config['missense-filter']['mpc']['field']], errors='coerce')
                    df[config['missense-filter']['cadd']['field']] = pd.to_numeric(df[config['missense-filter']['cadd']['field']], errors='coerce')
                    if config['missense-filter']['condition'] == 'cadd_if_no_mpc':
                        print('must pass the MPC filter, if the MPC is unavailable, must pass the CADD.')
                        df = df[ 
                            (
                                df['impact'].isin(['missense', 'missense_variant']) & 
                                (df[config['missense-filter']['mpc']['field']] >= config['missense-filter']['mpc']['min']) & 
                                (df[config['missense-filter']['mpc']['field']] < config['missense-filter']['mpc']['max'])
                            ) |
                            (
                                df['impact'].isin(['missense', 'missense_variant']) & 
                                (df[config['missense-filter']['mpc']['field']] == -1) & 
                                (df[config['missense-filter']['cadd']['field']] >= config['missense-filter']['cadd']['min']) &
                                (df[config['missense-filter']['cadd']['field']] < config['missense-filter']['cadd']['max'])
                            ) |
                            ( ~df['impact'].isin(['missense', 'missense_variant']) )
                        ]
                    elif config['missense-filter']['condition'] == 'cadd_and_mpc':
                        print('must pass both the MPC and the CADD filters.')
                        df = df[ 
                            (
                                df['impact'].isin(['missense', 'missense_variant']) & 
                                (df[config['missense-filter']['mpc']['field']] >= config['missense-filter']['mpc']['min']) & 
                                (df[config['missense-filter']['mpc']['field']] < config['missense-filter']['mpc']['max']) & 
                                (df[config['missense-filter']['cadd']['field']] >= config['missense-filter']['cadd']['min']) &
                                (df[config['missense-filter']['cadd']['field']] < config['missense-filter']['cadd']['max'])
                            ) |
                            ( ~df['impact'].isin(['missense', 'missense_variant']) )
                        ]
                    elif config['missense-filter']['condition'] == 'cadd_or_mpc':
                        print('must pass the MPC filter OR the CADD filter.')
                        df = df[ 
                            (
                                df['impact'].isin(['missense', 'missense_variant']) & 
                                (df[config['missense-filter']['mpc']['field']] >= config['missense-filter']['mpc']['min']) & 
                                (df[config['missense-filter']['mpc']['field']] < config['missense-filter']['mpc']['max'])
                            ) |
                            (
                                df['impact'].isin(['missense', 'missense_variant']) & 
                                (df[config['missense-filter']['cadd']['field']] >= config['missense-filter']['cadd']['min']) &
                                (df[config['missense-filter']['cadd']['field']] < config['missense-filter']['cadd']['max'])
                            ) |
                            ( ~df['impact'].isin(['missense', 'missense_variant']) )
                        ]
                    elif config['missense-filter']['condition'] == 'mpc_only':
                        print('must pass the MPC filter.')
                        df = df[ 
                            (
                                df['impact'].isin(['missense', 'missense_variant']) & 
                                (df[config['missense-filter']['mpc']['field']] >= config['missense-filter']['mpc']['min']) & 
                                (df[config['missense-filter']['mpc']['field']] < config['missense-filter']['mpc']['max'])
                            ) |
                            ( ~df['impact'].isin(['missense', 'missense_variant']) )
                        ]
                    elif config['missense-filter']['condition'] == 'cadd_only':
                        print('must pass the CADD filter.')
                        df = df[ 
                            (
                                df['impact'].isin(['missense', 'missense_variant']) & 
                                (df[config['missense-filter']['cadd']['field']] >= config['missense-filter']['cadd']['min']) &
                                (df[config['missense-filter']['cadd']['field']] < config['missense-filter']['cadd']['max'])
                            ) |
                            ( ~df['impact'].isin(['missense', 'missense_variant']) )
                        ]
                    else:
                        print('no specific filters applied to missenses.')
                print('after missense filtering:', len(df), 'transcripts impacted')

            # filters specific to inframe variants
            # TODO

            # filtering on frequency
            if 'gnomad-filter' in config:
                df[config['gnomad-filter']['field']] = pd.to_numeric(df[config['gnomad-filter']['field']], errors='coerce')
                df = df[
                    (df[config['gnomad-filter']['field']] >= config['gnomad-filter']['min']) &
                    (df[config['gnomad-filter']['field']] <= config['gnomad-filter']['max'])
                    ]
                print('after gnomad filtering:', len(df), 'transcripts impacted')

            # sort by transcript "importance" depending on config file priority
            # make categorical for sort to work on the following categories: impact, LoF, canonical...
            df['impact-category'] = df['impact'].map(dict_rev_impacts, na_action='ignore')
            df['impact-category'] = pd.Categorical(df['impact-category'], categories = ['lof_high','lof_med', 'genic_high', 'genic_med', 'genic_low', 'other_high', 'other_low'], ordered = True)
            df['canonical'] = pd.Categorical(df['canonical'], categories = ['YES', ''], ordered = True)
            df['loftee'] = pd.Categorical(df['loftee'], categories = ['HC', 'OS', '', 'LC'], ordered = True)
            df.sort_values(['sample_id', 'chr:pos:ref:alt', 'ENSG']+config['ordering-priority'], inplace=True)

            # aggregating transcripts is done by droping duplicates and keeping only the first (as we sorted using our preferences)
            df.drop_duplicates(subset = ['sample_id', 'chr:pos:ref:alt', 'ENSG'], keep = 'first', inplace=True)
            print('after remerging transcripts:', len(df), 'variant/gene/sample')

            # filtering on pext
            if 'pext-filter' in config and (len(df)>0):
                df[['chr', 'position', 'ref', 'alt']] = df['chr:pos:ref:alt'].str.split(':', expand=True)
                def variant_len(variant):
                        v = variant.split(':')
                        return( abs( len(v[2]) - len(v[3]) ) )
                df['variant_size'] = df['chr:pos:ref:alt'].apply(variant_len)

                df_pext = pd.read_csv(config['pext-filter']['file'], sep='\t')
                df_pext.columns = ['Chromosome', 'Start', 'End', 'mean_brain', 'ensg', 'symbol']
                gr_pext = pr.PyRanges(df_pext)

                def get_pext2(gr_pext, ensg, symbol, chrom, position, impact, variant_size):
                    shift = 0
                    if impact in ['splice_donor', 'splice_acceptor']:
                        shift = 3

                    end = int(position)+shift+variant_size+1
                    start = int(position)-shift-variant_size

                    df_temp = gr_pext[chrom, start:end].as_df()
                    if df_temp.empty :
                        return -1
                    df_temp = df_temp[(df_temp['ensg']==ensg) | (df_temp['symbol']==symbol)]

                    if len(df_temp)>1:
                        return df_temp['mean_brain'].max()
                    if len(df_temp)==1:
                        return df_temp['mean_brain'].item()
                    return -1

                df[config['pext-filter']['field']] = df.apply(lambda x: get_pext2(gr_pext, x['ENSG'], x['symbol'], x['chr'], x['position'], x['impact'], x['variant_size']), axis=1)
                df = df[df[config['pext-filter']['field']]>=config['pext-filter']['min']]
                df.drop(['chr', 'position', 'ref', 'alt', 'variant_size'], axis=1, inplace=True)
                print('after pext filtering:', len(df), 'transcripts impacted')

            # outputing processed file
            if chunk_nb==1:
                df.to_csv(args.output, sep='\t', index=False)
            else:
                df.to_csv(args.output, sep='\t', index=False, mode='a', header=None)

def main(args=None):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('configuration', help='config file')
    parser.add_argument('slivar', help='slivar file to reannotate')
    parser.add_argument('output', help='annotated slivar file')
    parser.add_argument('--chunksize', default=100000, help='size of the chunks read from the input (default 100000)', type=int)

    reannotate(parser.parse_args(args))