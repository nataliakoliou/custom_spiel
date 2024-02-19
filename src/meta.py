class Metagame:
    def __init__(self, utilities, alpha, profiles=2):
        self.utilities = utilities
        self.alpha = alpha
        self.profiles = profiles

    def alpharank(self):
        payoffs = self.transform()
        hpt = utils.check_payoffs_are_hpt(payoffs)  # hpt = False
        labels = utils.get_strat_profile_labels(payoffs, hpt)
        rhos, rho_m, pi, _, _ = alpharank.compute(payoffs, alpha=self.alpha)
        alpharank.print_results(payoffs, hpt, rhos=rhos, rho_m=rho_m, pi=pi)
        utils.print_rankings_table(payoffs, pi, labels)
        net_plotter = alpharank_visualizer.NetworkPlot(payoffs, rhos, rho_m, pi, labels, num_top_profiles=self.profiles)
        net_plotter.compute_and_draw_network()

    def transform(self):
        #use self.utilities to reconstruct it in a payoff table format