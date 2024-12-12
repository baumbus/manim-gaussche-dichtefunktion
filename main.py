from manim import *

class Count(Animation):
    def __init__(self, number: DecimalNumber, start: float, end: float, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(number,  **kwargs)
        # Set start and end
        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        # Set value of DecimalNumber according to alpha
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)


class Gausschedichtefunktion(Scene):
    def construct(self):
        label_size = 36
        graph_color = MAROON
        title_size = 32
        
        grid = Axes( 
            x_range=[-4, 4, 1],  # step size determines num_decimal_places.
            y_range=[0, 1, 0.1],
            axis_config={
                "include_numbers": True,
            },
            tips=False,
        ).set_z_index(10)
        
        grid_wider = Axes( 
            x_range=[-8, 8, 1],  # step size determines num_decimal_places.
            y_range=[0, 1, 0.1],
            axis_config={
                "include_numbers": True,
            },
            tips=False,
        ).set_z_index(10)

        mu = DecimalNumber(0, font_size=label_size)
        sigma = DecimalNumber(1, font_size=label_size)

        mu_label = MathTex(r'\mu =', font_size=label_size)
        sigma_label = MathTex(r'\sigma =', font_size=label_size)

        mu_label.to_corner(UL)
        mu.next_to(mu_label, RIGHT)
        sigma_label.next_to(mu_label, DOWN)
        sigma.next_to(sigma_label, RIGHT)

        label_group = VGroup(mu_label, sigma_label, mu, sigma)    
        
        def base_function(x):
            return np.e ** (-(1/2) * x ** 2)  
        
        def verschiebare_function(x):
            return np.e ** (-(1/2) * (x - mu.get_value()) ** 2)  
        
        def stauchbare_function(x):
            return np.e ** (-(1/2) * ((x - mu.get_value()) / sigma.get_value()) ** 2)
        
        def dichte_function(x):
            return (1 / (sigma.get_value() * np.sqrt(2 * np.pi))) * np.e ** (-(1/2) * ((x - mu.get_value()) / sigma.get_value()) ** 2)
        
        base = grid.plot(base_function, color=graph_color)
        
        moving = always_redraw(
            lambda: grid_wider.plot(verschiebare_function, color=graph_color)
        )
        
        streching = always_redraw(
            lambda: grid_wider.plot(stauchbare_function, color=graph_color)
        )
        
        final = always_redraw(
            lambda: grid_wider.plot(dichte_function, color=graph_color)
        )
        
        title = Title(
            r"$f(x)=e^{-\frac{1}{2}x^2}$",
            include_underline=False,
            font_size=title_size,
        )
        
        title.shift(UP * 0.3)
        title.set_z_index(10)
        
        moving_title = Title(
            r"$f(x)=e^{-\frac{1}{2} \cdot (x - \mu)^2}$",
            include_underline=False,
            font_size=title_size,
        )
        
        moving_title.shift(UP * 0.3)
        moving_title.set_z_index(10)
        
        streching_title = Title(
            r"$f(x)=e^{-\frac{1}{2}\cdot \left(\frac{x - \mu}{\sigma}\right)^2}$",
            include_underline=False,
            font_size=title_size,
        )
        
        streching_title.shift(UP * 0.3)
        streching_title.set_z_index(10)
        
        final_title = Title(
            r"$f(x)=\frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{1}{2}\cdot \left(\frac{x - \mu}{\sigma}\right)^2}$",
            include_underline=False,
            font_size=title_size,
        )
        
        final_title.shift(UP * 0.3)
        final_title.set_z_index(10)

        self.play(
            FadeIn(grid, shift=UP)
        )

        self.play(FadeIn(title))
        self.play(Create(label_group, lag_ratio=0.1))

        self.next_section("Fade in e^-1/2x^2")
        self.play(FadeIn(base))

        self.wait(5)
        self.next_section("Verschiebare Funktion")
        self.play(FadeOut(base))
        self.play(FadeTransform(grid, grid_wider, stretch=True))
        self.play(TransformMatchingTex(title, moving_title))
        self.play(FadeIn(moving))
        self.wait(2)
        self.play(Count(mu, 0, 4), run_time=2)
        self.play(Count(mu, 4, 2), run_time=1)
        self.play(Count(mu, 2, -2), run_time=2)
        self.play(Count(mu, -2, 0), run_time=2)
        
        self.next_section("Stauchbare Funktion")
        self.play(FadeOut(moving))
        self.play(TransformMatchingTex(moving_title, streching_title))
        self.play(FadeIn(streching))
        self.wait(2)
        self.play(Count(sigma, 1, 2), run_time=2)
        self.play(Count(sigma, 2, 4), run_time=2)
        self.play(Count(sigma, 4, 1), run_time=2)
        
        self.next_section("Finale Funktion")
        self.play(FadeOut(streching))
        self.play(TransformMatchingTex(streching_title, final_title))
        self.play(FadeIn(final))
        self.wait(2)
        self.play(Count(mu, 0, 4), run_time=2)
        self.play(Count(sigma, 1, 2), run_time=2)
        self.play(Count(mu, 4, 2), run_time=1)
        self.play(Count(sigma, 2, 4), run_time=2)
        self.play(Count(mu, 2, -2), run_time=2)
        self.play(Count(sigma, 4, 1), run_time=2)
        self.play(Count(mu, -2, 0), run_time=2)

        self.next_section("Fade out everything")
        
        self.play(FadeOut(VGroup(final_title, final, grid_wider)))
        self.play(FadeOut(label_group))
        
        self.wait(2)
