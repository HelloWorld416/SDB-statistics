"""Rebuild v2 aggregates; preserve the published video corpus and event taxonomy."""
import argparse,bisect,csv,hashlib,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_csv(name,rows):
    with (ROOT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,row))+' |' for row in rows])+'\n\n'
def percentage(n,d):return round(100*n/d,4)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--release',type=Path,default=ROOT.parent/'StreamDriveBench-release/data');a=p.parse_args();data=a.release
    base=read(Path(__file__).with_name('video_and_taxonomy_baseline.json'));manifest=read(data/'release_manifest.json')
    for name,h in manifest['files'].items():assert sha(data/name)==h,name
    qs=read(data/'model_inputs.json');groups=read(data/'event_groups.json');summary=read(data/'summary.json');labels=read(data/'labels.json')
    eps={e['episode_id']:e for e in read(data/'episodes_metadata.json')['episodes']}
    lookup={q['query_id']:q for q in qs};assert len(qs)==len(lookup)==1935
    links=[qid for g in groups for qid in g['query_ids']]
    assert len(links)==len(set(links))==1935 and set(links)==set(lookup)
    assert len(groups)==len({g['group_id'] for g in groups})==len({(g['dataset'],g['episode_id'],g['event_id']) for g in groups})==815
    for g in groups:
        families={lookup[qid]['family'] for qid in g['query_ids']}
        assert len(families)==len(g['query_ids']) and families==set(g['families'])
        assert g['family_complete']==(len(families)==3)
        for qid in g['query_ids']:
            assert lookup[qid]['episode_id']==g['episode_id'] and lookup[qid]['dataset']==g['dataset']
            assert labels[qid]['group_id']==g['group_id']
    names={'HGI':'History QA','AD':'Prediction QA','ETP':'Event QA'};fc=Counter(q['family'] for q in qs)
    assert dict(fc)==summary['by_family']=={'HGI':700,'AD':552,'ETP':683}
    covered=len({q['episode_id'] for q in qs});assert covered==summary['QA_videos']==504
    categories=Counter(g['event_category'] for g in groups);negative='Verified non-triggering event'
    mapping=base['event_mapping'];assert set(categories)=={r['event_type'] for r in mapping}|{negative}
    ng=[g for g in groups if g['event_category']==negative]
    assert len(ng)==110 and all(len(g['query_ids'])==1 and g['families']==['ETP'] for g in ng)
    assert all(labels[g['query_ids'][0]]['ground_truth']['outcome']=='not_observed_within_window' for g in ng)
    classified=len(groups)-len(ng)
    def qcounts(gs):return Counter(lookup[qid]['family'] for g in gs for qid in g['query_ids'])
    def family_columns(c):return {name:c[f] for f,name in names.items()}
    qa_rows=[dict(qa_type=name,queries=fc[f],percentage=percentage(fc[f],len(qs))) for f,name in names.items()];write_csv('qa_type_counts.csv',qa_rows)
    source_rows=[]
    for row in base['sources']:
        ds=row['dataset'];c=Counter(q['family'] for q in qs if q['dataset']==ds)
        source_rows.append(dict(dataset=ds,videos=row['videos'],selected_hours=row['hours'],**family_columns(c),QA_total=sum(c.values()),event_groups=sum(g['dataset']==ds for g in groups)))
    assert sum(r['videos'] for r in source_rows)==648
    assert sum(r['QA_total'] for r in source_rows)==1935 and sum(r['event_groups'] for r in source_rows)==815
    write_csv('dataset_counts.csv',source_rows)
    event_rows=[]
    for cat,n in sorted(categories.items(),key=lambda x:(x[0]==negative,-x[1],x[0])):
        c=qcounts([g for g in groups if g['event_category']==cat])
        event_rows.append(dict(event_type=cat,event_type_zh=base['event_names_zh'].get(cat,'已核验未触发事件（负例补充项）'),events=n,percentage=percentage(n,len(groups)),**family_columns(c),QA_total=sum(c.values())))
    write_csv('event_type_counts.csv',event_rows)
    macro_rows=[];order=list(dict.fromkeys((r['category_zh'],r['category_en']) for r in mapping))
    for zh,en in order:
        cats={r['event_type'] for r in mapping if r['category_en']==en};gs=[g for g in groups if g['event_category'] in cats];c=qcounts(gs)
        macro_rows.append(dict(category_zh=zh,category_en=en,events=len(gs),event_percentage=percentage(len(gs),classified),all_event_percentage=percentage(len(gs),len(groups)),**family_columns(c),QA_total=sum(c.values())))
    write_csv('event_macro_counts.csv',macro_rows)
    write_csv('event_macro_mapping.csv',[dict(row,events=categories[row['event_type']]) for row in mapping])
    write_csv('event_negative_supplement.csv',[event_rows[-1]])
    assert sum(r['events'] for r in macro_rows)==classified==705
    assert sum(r['QA_total'] for r in macro_rows)+110==1935
    assert sum(r['events'] for r in event_rows)==815 and sum(r['QA_total'] for r in event_rows)==1935
    assert all(sum(r[name] for r in event_rows)==fc[f] for f,name in names.items())
    edges=[0,30,90,180,300,600,1200,1800];bins=[0]*7
    for q in qs:
        ep=eps[q['episode_id']];t=q['query_second']-ep['selection_start_sec'];assert 0<=t<1800
        assert q['query_second']<=ep['selection_end_sec']
        bins[bisect.bisect_right(edges,t)-1]+=1
    assert sum(bins)==1935
    temporal=[dict(interval_sec=f'{lo}-{hi}',start_sec=lo,end_sec=hi,queries=n,percentage=percentage(n,1935)) for lo,hi,n in zip(edges,edges[1:],bins)]
    write_csv('queries_temporal_distribution.csv',temporal)
    sizes=Counter(len(g['query_ids']) for g in groups);strict=sum(g['family_complete'] and g['strict_source_link'] for g in groups)
    assert sizes=={3:444,2:232,1:139} and strict==66
    outcomes=Counter(labels[q['query_id']]['ground_truth']['outcome'] for q in qs if q['family']=='ETP')
    assert outcomes=={'positive':572,'not_observed_within_window':111}
    lines=[];add=lines.append
    add('# StreamDriveBench release statistics — 1,935 QA\n')
    add('统计分支：**v2**。数据版本：**StreamDriveBench-1935-v1**。统计日期：2026-10-31。QA 与事件统计来自当前最终 release；视频总量、时长分布、三类 QA 名称和四大类／14 小类映射沿用原统计版本。\n')
    add('## 1. 总体规模与统计口径\n')
    add(table(['指标','数值'],[['视频总数',648],['总选用时长（论文展示）','100 h'],['总选用时长（沿用素材统计，小时）','100.00445718'],['总选用时长（沿用素材统计，秒）','360016.045836'],['QA 总数',1935],['QA 关联事件组总数（含独立负例组）',815],['原 14 个行为小类中的事件组',705],['独立未触发负例事件组',110],['行为小类数',14],['QA 覆盖视频数',504]]))
    add('整体素材仍为 **648 个视频、约 100 小时**。第 3 节的视频时长分布完整沿用原分支，未用最终 QA 覆盖的 504 个视频重新计算素材总量。时长是选用片段长度，不是完整下载视频时长或每题输入窗口之和。\n')
    add('“事件数量与 1,935 条 QA 对齐”表示只计这些问题实际关联的事件，以 `(dataset, episode_id, event_id)` 去重；一组可关联多条 QA，因此是 **815 个事件组**，不是 1,935 个独立事件。所有 QA 已按正式 release 标为人工审核通过；该状态不等于事件分类或三题严格关联关系均经过独立人工验收。\n')
    add('## 2. 三类 QA 数量\n')
    add(table(['QA 类型','数量','占全部 QA 的比例（%）'],[[r['qa_type'],r['queries'],f"{r['percentage']:.4f}"] for r in qa_rows]+[['Total',1935,'100.0000']]))
    add('三类名称统一为 **History QA、Prediction QA、Event QA**，分别对应历史理解、短期预测和事件触发响应。\n')
    add('### 按数据来源统计\n')
    add(table(['数据源','视频数量','选用时长（h）',*names.values(),'QA 合计','事件组数量'],[list(r.values()) for r in source_rows]+[['Total',648,'100.004457',700,552,683,1935,815]]))
    add(base['video_duration_section'].rstrip()+'\n')
    add('## 4. 驾驶事件类型与数量\n')
    add('沿用当前 release 的 `event_category`。下表百分比分母为 **815 个 QA 关联事件组**；每个事件组只计一次。原有 14 个行为小类继续保留，新增 release 标签 `Verified non-triggering event` 单列为负例补充项，不将其视为第 15 种已发生的驾驶行为。\n')
    add(table(['Event type','中文类别','事件组数量','占全部事件组（%）',*names.values(),'QA 合计'],[[r['event_type'],r['event_type_zh'],r['events'],f"{r['percentage']:.4f}",*[r[x] for x in names.values()],r['QA_total']] for r in event_rows]+[['Total','合计',815,'100.0000',700,552,683,1935]]))
    add('类别为 release 保存的描述性标记，未重新对修订后的每道题进行语义分类。尤其普通上下文关联组的三道题可能涉及不同状态变化，表中 QA 按所属事件组的类别汇总。\n')
    add('### 四个事件大类\n')
    add('小类到大类的映射与原分支一致；**Other transitions、Visibility changes、Multiple transition types 仍归入长尾事件**。四个大类涵盖 705 个有原分类标签的事件组；大类内部占比的分母为 705，另列以全部 815 组为分母的比例。110 个独立未触发负例组不强行归入某种驾驶行为，也不并入长尾事件。\n')
    rows=[]
    for r in macro_rows:
        types='；'.join(f"{m['event_type']} ({categories[m['event_type']]})" for m in mapping if m['category_en']==r['category_en'])
        rows.append([r['category_zh'],r['category_en'],types,r['events'],f"{r['event_percentage']:.4f}",f"{r['all_event_percentage']:.4f}"])
    add(table(['大类','English label','包含的小类（事件组数）','事件组数量','占四类合计（%）','占全部事件组（%）'],rows+[['四类合计','Total classified','14 个小类',705,'100.0000',f'{percentage(705,815):.4f}'],['负例补充项','Verified non-triggering event','不属于四个行为大类',110,'—',f'{percentage(110,815):.4f}'],['全体合计','Total','',815,'—','100.0000']]))
    add('“车辆运动行为”包含自车及其他车辆的方向、车道和速度变化；“交通交互与参与者状态”包含相对运动、穿行、行人／骑行者动作和灯光状态；“道路与场景变化”包含交通设施状态及通行进程。不能将车辆运动行为直接等同于自车行为。\n')
    add('#### 大类对应的三类 QA 数量\n')
    add(table(['大类',*names.values(),'QA 合计'],[[r['category_zh'],*[r[x] for x in names.values()],r['QA_total']] for r in macro_rows]+[['负例补充项（不属于四类）',0,0,110,110],['合计',700,552,683,1935]]))
    add('绘图数据：[大类统计 CSV](event_macro_counts.csv) · [分类映射 CSV](event_macro_mapping.csv) · [全部事件类别 CSV](event_type_counts.csv) · [独立负例补充 CSV](event_negative_supplement.csv)。`event_macro_counts.csv` 中 `event_percentage` 以 705 为分母，`all_event_percentage` 以 815 为分母。\n')
    add('### 事件组的三类 QA 组成\n')
    add(table(['事件组组成','事件组数量','贡献 QA 数量'],[['三类齐全',444,1332],['包含两类',232,464],['包含一类',139,139],['Total',815,1935]]))
    add('444 个三类齐全组中，66 组具有源标注的严格关联标记，378 组为普通上下文关联。Event QA 包含 **572 条正例、111 条未触发负例**；其中 110 条组成上述独立负例组，另 1 条仍在原分类的事件组内，因此不能将 110 解释为全部负例数。\n')
    add('## 5. Queries Temporal Distribution\n')
    add('将三类 QA 合并，每条问题计一次；时间为 `query_second - selection_start_sec`，相对于选用片段起点。Event QA 使用问题注入时刻，不使用事件触发或轮询时刻。保持原来的七个左闭右开区间，百分比分母改为 1,935。\n')
    add(table(['片段内提问时间区间（s）','QA 数量','占全部 QA（%）'],[[f"[{r['start_sec']}, {r['end_sec']})",r['queries'],f"{r['percentage']:.4f}"] for r in temporal]+[['Total',1935,'100.0000']]))
    add('绘图时使用单个数据系列；横轴为 **Time since selected clip start (s)**，纵轴为 **Number of queries**。数量依次为 `'+', '.join(map(str,bins))+'`。区间宽度不等，按区间类别绘制柱状图，柱高表示数量。\n')
    add('绘图数据：[Queries Temporal Distribution CSV](queries_temporal_distribution.csv)。\n')
    add('## 6. 绘图与复现说明\n')
    add('- 视频分布沿用 `145, 220, 155, 58, 70, 0`，分母 648。\n- QA 分布为 `700, 552, 683`，分母 1,935。\n- 全部事件组分布含负例补充项，分母 815；四个原大类内部分布的分母为 705。\n- CSV 百分比以 0–100 表示，均不含合计行。用整数计数计算比例可避免舍入累计误差。\n')
    add('本分支从 GitHub 已发布统计提交 `'+base['base_commit']+'` 创建，原分支保留 4,013 条版本。视频素材基线与分类映射固定保存在 [video_and_taxonomy_baseline.json](scripts/video_and_taxonomy_baseline.json)，当前 release 的视频目录仅覆盖 504 个 QA 视频，不用于覆盖完整素材基线。\n')
    add('底层字段对应：`HGI → History QA`，`AD → Prediction QA`，`ETP → Event QA`。本次只更新统计，不修改 release。\n')
    add('复现命令：\n\n```bash\npython scripts/build_v2_statistics.py --release /path/to/StreamDriveBench-release/data\n```\n')
    inputs=['release_manifest.json','model_inputs.json','episodes_metadata.json','event_groups.json','summary.json','labels.json']
    hashes={name:sha(data/name) for name in inputs}
    add(table(['源文件','SHA-256'],[[k,v] for k,v in hashes.items()]))
    add('校验结果：release 全部文件哈希匹配 manifest；1,935 个唯一 query_id 全部且仅归属一个事件组；815 个事件组无重复；分类、来源和提问时间分布计数均与最终 release 一致。视频时长章节与原已发布版本逐字一致。\n')
    (ROOT/'README.md').write_text('\n'.join(lines))
    report=dict(version=manifest['version'],date='2026-10-31',status='passed',queries=len(qs),by_family=dict(fc),event_groups=len(groups),classified_event_groups=705,independent_negative_event_groups=110,QA_videos=covered,video_corpus=dict(videos=648,hours=base['hours'],source_commit=base['base_commit']),group_sizes=dict(sizes),strict_full_groups=strict,temporal_counts=bins,source_sha256=hashes)
    (ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
