import matplotlib.pyplot as plt
import numpy as np

def plot_auc(gsearch_lr):
    plt.figure(figsize=(19, 7))
    plt.xlabel("Regularization Parameter")
    plt.ylabel("Score")
    plt.grid()
    
    scoring={'AUC': 'roc_auc'}
    ax = plt.axes()
    results = gsearch_lr.cv_results_
    
    # Get the regular numpy array from the MaskedArray
    X_axis = np.log10( np.array(results['param_C'].data, dtype=float))
    
    for scorer, color, fig_no, ylim in zip(sorted(scoring), ['g'],[1],[[0,1.2]]):
        
        for sample, style in (('train', '--'), ('test', '-')):
            ax = plt.subplot(1,2,fig_no)
            ax.set_ylim(ylim)
            sample_score_mean = results['mean_%s_%s' % (sample, scorer)]
            sample_score_std = results['std_%s_%s' % (sample, scorer)]
            ax.fill_between(X_axis, sample_score_mean - sample_score_std,
                            sample_score_mean + sample_score_std,
                            alpha=0.1 if sample == 'test' else 0, color=color)
            ax.plot(X_axis, sample_score_mean, style, color=color,
                    alpha=1 if sample == 'test' else 0.7,
                    label="%s (%s)" % (scorer, sample))

        best_index = np.nonzero(results['rank_test_%s' % scorer] == 1)[0][0]
        best_score = results['mean_test_%s' % scorer][best_index]
        
        # Plot a dotted vertical line at the best score for that scorer marked by x
        ax.plot([X_axis[best_index], ] * 2, [0, best_score],
                linestyle='-.', color=color, marker='x', markeredgewidth=3, ms=8)
            
        # Annotate the best score for that scorer
        ax.annotate("%0.3f" % best_score,
                    (X_axis[best_index], best_score + 0.005))
        ax.legend(loc="best")
        plt.xlabel("log(Regularization Param C)")

    plt.grid('off')
    plt.show()
