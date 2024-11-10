import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import threading

class TreeBusinessGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Email Pattern Analyzer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1E1E1E')  # Dark background

        # Define colors with better contrast
        self.primary_color = "#1A237E"  # Darker blue
        self.accent_color = "#4CAF50"  # Green
        self.success_color = "#00C853"  # Bright green
        self.warning_color = "#F44336"  # Red
        self.bg_color = "#2C2C2C"  # Dark gray
        self.text_color = "white"  # White
        self.black = "#000000"
        self.button_hover = "#000000"  # Light blue for hover
        self.button_active = "#283593"  # Darker blue for click
        self.disabled_color = "#666666"  # Gray for disabled state

        # Button styles
        self.button_style = {
            'font': ('Arial', 12, 'bold'),
            'borderwidth': 2,
            'relief': 'raised',
            'cursor': 'hand2',
            'padx': 20,
            'pady': 5
        }

        # Initialize other variables
        self.df = None
        self.df2 = None
        self.df3 = None
        self.processed_df = None
        self.processed_df2 = None
        self.processed_df3 = None
        self.email_patterns = {}

        # Setup GUI
        self.setup_gui()

    def create_styled_button(self, parent, text, command, is_important=False):
        """Helper method to create consistently styled buttons"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=self.button_style['font'],
            bg=self.accent_color if is_important else self.primary_color,
            fg=self.text_color,
            activebackground=self.button_active,
            activeforeground=self.text_color,
            disabledforeground=self.disabled_color,
            **self.button_style
        )

        # Bind hover events
        btn.bind('<Enter>', lambda e: btn.config(bg=self.button_hover))
        btn.bind('<Leave>', lambda e: btn.config(
            bg=self.accent_color if is_important else self.primary_color))

        return btn
    def setup_gui(self):
        # Heading Section
        heading_frame = tk.Frame(self.root, bg=self.primary_color)
        heading_frame.pack(fill='x', pady=10)

        heading_label = tk.Label(
            heading_frame,
            text="Tree Business Solutions",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg=self.primary_color,
            padx=20,
            pady=10
        )
        heading_label.pack()

        # Main container for all sections
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill='both', expand=True, padx=10, pady=5)

        # Section 1: Pattern Analysis
        section1_frame = tk.LabelFrame(
            main_container,
            text="Pattern Analysis",
            font=('Arial', 12, 'bold'),
            bg=self.bg_color,
            fg=self.primary_color
        )
        section1_frame.pack(fill='x', pady=5)

        # Upload Section 1
        self.setup_pattern_analysis_section(section1_frame)

        # Section 2: Email Prediction
        section2_frame = tk.LabelFrame(
            main_container,
            text="Email Prediction",
            font=('Arial', 12, 'bold'),
            bg=self.bg_color,
            fg=self.text_color
        )
        section2_frame.pack(fill='x', pady=5)

        # Upload Section 2
        self.setup_email_prediction_section(section2_frame)

        # Section 3: Email Predictor
        section3_frame = tk.LabelFrame(
            main_container,
            text="Email Predictor",
            font=('Arial', 12, 'bold'),
            bg=self.bg_color,
            fg=self.text_color
        )
        section3_frame.pack(fill='x', pady=5)

        # Upload Section 3
        self.setup_email_predictor_section(section3_frame)

        # Results Section
        results_frame = tk.LabelFrame(
            main_container,
            text="Results Preview",
            font=('Arial', 12, 'bold'),
            bg='black',
            fg=self.text_color,
            padx=15,
            pady=15
        )
        results_frame.pack(fill='both', expand=True, pady=5)

        # Treeview setup
        style = ttk.Style()
        style.configure(
            "Treeview",
            background="",
            fieldbackground="black",
            rowheight=25
        )
        style.configure(
            "Treeview.Heading",
            font=('Arial', 10, 'bold'),
            background=self.primary_color,
            foreground="white"
        )

        self.tree = ttk.Treeview(
            results_frame,
            columns=('client', 'domain', 'format', 'email'),
            show='headings',
            height=15
        )

        # Configure tree columns
        self.tree.heading('client', text='Client')
        self.tree.heading('domain', text='Domain')
        self.tree.heading('format', text='Email Format')
        self.tree.heading('email', text='Email generated')

        self.tree.column('client', width=200)
        self.tree.column('domain', width=150)
        self.tree.column('format', width=150)
        self.tree.column('email', width=200)

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(results_frame, orient='horizontal', command=self.tree.xview)

        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')

        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(0, weight=1)

        # Download Buttons Frame
        download_frame = tk.Frame(main_container, bg='white')
        download_frame.pack(fill='x', pady=10)

        # Download buttons
        self.download_button = tk.Button(
            download_frame,
            text="Download Pattern Results",
            command=self.save_results,
            state='disabled',
            font=('Arial', 12, 'bold'),
            bg=self.success_color,
            fg='white',
            padx=30,
            pady=10,
            cursor='hand2',
            relief='flat'
        )
        self.download_button.pack(side='right', padx=20)

        self.download_button2 = tk.Button(
            download_frame,
            text="Download Predicted Emails",
            command=self.save_results2,
            state='disabled',
            font=('Arial', 12, 'bold'),
            bg=self.success_color,
            fg='white',
            padx=30,
            pady=10,
            cursor='hand2',
            relief='flat'
        )
        self.download_button2.pack(side='right', padx=20)

        self.download_button3 = tk.Button(
            download_frame,
            text="Download Emails from Predictor",
            command=self.save_results3,
            state='disabled',
            font=('Arial', 12, 'bold'),
            bg=self.success_color,
            fg='white',
            padx=30,
            pady=10,
            cursor='hand2',
            relief='flat'
        )
        self.download_button3.pack(side='right', padx=20)

        self.run()

    def setup_pattern_analysis_section(self, parent_frame):
        # Implement the Pattern Analysis section here
        upload_frame = tk.Frame(parent_frame, bg=self.bg_color)
        upload_frame.pack(fill='x', pady=5)

        self.file_label = tk.Label(
            upload_frame,
            text="No file selected",
            font=('Arial', 12),
            fg=self.warning_color,
            bg=self.bg_color,
            padx=10,
            pady=5
        )
        self.file_label.pack(side='left', padx=10)

        self.upload_button = tk.Button(
            upload_frame,
            text="Upload Pattern CSV",
            command=self.upload_file,
            font=('Arial', 12, 'bold'),
            bg=self.accent_color,
            fg='black',
            padx=20,
            pady=5,
            cursor='hand2',
            relief='flat'
        )
        self.upload_button.pack(side='right', padx=10)

        progress_frame = tk.Frame(parent_frame, bg=self.bg_color)
        progress_frame.pack(fill='x', pady=5)

        self.progress_bar1 = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            value=0,
            length=800
        )
        self.progress_bar1.pack(side='left', padx=10)

        self.status_label1 = tk.Label(
            progress_frame,
            text="Ready",
            font=('Arial', 12),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.status_label1.pack(side='left', padx=10)

        self.process_button = tk.Button(
            progress_frame,
            text="Process Patterns",
            command=self.process_file,
            state='disabled',
            font=('Arial', 12, 'bold'),
            bg=self.success_color,
            fg='black',
            padx=20,
            pady=5,
            cursor='hand2',
            relief='flat'
        )
        self.process_button.pack(side='right', padx=10)
    def setup_email_prediction_section(self, parent_frame):
        # Implement the Email Prediction section here
        upload_frame2 = tk.Frame(parent_frame, bg=self.bg_color)
        upload_frame2.pack(fill='x', pady=5)

        self.file_label2 = tk.Label(
            upload_frame2,
            text="No file selected",
            font=('Arial', 12),
            fg=self.warning_color,
            bg=self.bg_color
        )
        self.file_label2.pack(side='left', padx=10)

        self.upload_button2 = tk.Button(
            upload_frame2,
            text="Upload Prediction CSV",
            command=self.upload_file2,
            font=('Arial', 12, 'bold'),
            bg=self.accent_color,
            fg='white',
            padx=20,
            pady=5,
            cursor='hand2',
            relief='flat'
        )
        self.upload_button2.pack(side='right', padx=10)

        progress_frame2 = tk.Frame(parent_frame, bg=self.bg_color)
        progress_frame2.pack(fill='x', pady=5)

        self.progress_bar2 = ttk.Progressbar(
            progress_frame2,
            mode='determinate',
            value=0,
            length=800
        )
        self.progress_bar2.pack(side='left', padx=10)

        self.status_label2 = tk.Label(
            progress_frame2,
            text="Ready",
            font=('Arial', 12),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.status_label2.pack(side='left', padx=10)

        self.process_button2 = tk.Button(
            progress_frame2,
            text="Generate Emails",
            command=self.process_file2,
            state='disabled',
            font=('Arial', 12, 'bold'),
            bg=self.black,
            fg='white',
            padx=20,
            pady=5,
            cursor='hand2',
            relief='flat'
        )
        self.process_button2.pack(side='right', padx=10)

    def setup_email_predictor_section(self, parent_frame):
        # Implement the Email Predictor section here
        upload_frame3 = tk.Frame(parent_frame, bg=self.bg_color)
        upload_frame3.pack(fill='x', pady=5)

        self.file_label3 = tk.Label(
            upload_frame3,
            text="No file selected",
            font=('Arial', 12),
            fg=self.warning_color,
            bg=self.bg_color
        )
        self.file_label3.pack(side='left', padx=10)

        self.upload_button3 = tk.Button(
            upload_frame3,
            text="Upload Predictor CSV",
            command=self.upload_file3,
            font=('Arial', 12, 'bold'),
            bg=self.accent_color,
            fg='white',
            padx=20,
            pady=5,
            cursor='hand2',
            relief='flat'
        )
        self.upload_button3.pack(side='right', padx=10)

        progress_frame3 = tk.Frame(parent_frame, bg=self.bg_color)
        progress_frame3.pack(fill='x', pady=5)

        self.progress_bar3 = ttk.Progressbar(
            progress_frame3,
            mode='determinate',
            value=0,
            length=800
        )
        self.progress_bar3.pack(side='left', padx=10)

        self.status_label3 = tk.Label(
            progress_frame3,
            text="Ready",
            font=('Arial', 12),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.status_label3.pack(side='left', padx=10)

        self.predict_button = tk.Button(
            progress_frame3,
            text="Predict Emails",
            command=self.predict_emails,
            state='disabled',
            font=('Arial', 12, 'bold'),
            bg=self.black,
            fg='white',
            padx=20,
            pady=5,
            cursor='hand2',
            relief='flat'
        )
        self.predict_button.pack(side='right', padx=10)

    def upload_file3(self):
        file_path = filedialog.askopenfilename(
            filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')]
        )
        if file_path:
            try:
                df = pd.read_csv(file_path)
                required_columns = ['First Name', 'Last Name', 'Email Format', 'Domain']

                if all(col.strip() in [col.strip() for col in df.columns] for col in required_columns):
                    self.df3 = df
                    self.file_label3.config(
                        text=f"Selected: {os.path.basename(file_path)}",
                        fg=self.success_color
                    )
                    self.predict_button.config(state='normal')
                    self.download_button3.config(state='normal')
                else:
                    messagebox.showerror("Error", f"Missing required columns. Required: {', '.join(required_columns)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error reading file: {str(e)}")
                self.file_label3.config(text="Error in file selection", fg=self.warning_color)

    def predict_emails(self):
        if self.df3 is None:
            messagebox.showerror("Error", "No prediction data available. Please upload a CSV file first.")
            return

        self.predict_button.config(state='disabled')
        self.status_label3.config(text="Predicting email addresses...")
        self.progress_bar3.config(value=0)
        threading.Thread(target=self._predict_thread, daemon=True).start()

    def show_results(self, df):
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert new data
            for _, row in df.iterrows():
                values = [
                    row['First Name'],
                    row['Last Name'],
                    row['Email Format'],
                    row['Domain'],
                    row['Email generated']
                ]
                self.tree.insert('', 'end', values=values)

        except Exception as e:
            print(f"Error showing results: {str(e)}")
            messagebox.showerror("Error", f"Error showing results: {str(e)}")

    def upload_file3(self):
        file_path = filedialog.askopenfilename(
            filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')]
        )
        if file_path:
            try:
                df = pd.read_csv(file_path)
                required_columns = ['First Name', 'Last Name', 'Email Format', 'Domain']

                if all(col.strip() in [col.strip() for col in df.columns] for col in required_columns):
                    self.df3 = df
                    self.file_label3.config(
                        text=f"Selected: {os.path.basename(file_path)}",
                        fg=self.success_color
                    )
                    self.predict_button.config(state='normal')
                    self.download_button3.config(state='normal')
                else:
                    messagebox.showerror("Error", f"Missing required columns. Required: {', '.join(required_columns)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error reading file: {str(e)}")
                self.file_label3.config(text="Error in file selection", fg=self.warning_color)

    def predict_emails(self):
        if self.df3 is None:
            messagebox.showerror("Error", "No prediction data available. Please upload a CSV file first.")
            return

        self.predict_button.config(state='disabled')
        self.status_label3.config(text="Predicting email addresses...")
        self.progress_bar3.config(value=0)
        threading.Thread(target=self._predict_thread, daemon=True).start()

    def _predict_thread(self):
        try:
            total_rows = len(self.df3)
            for i, _ in enumerate(self.df3.iterrows()):
                result_df = self.generate_predicted_emails()
                self.show_results(result_df)
                self.progress_bar3.config(value=(i + 1) / total_rows * 100)
                self.root.update()
            self.status_label3.config(text="Email prediction complete!", fg=self.success_color)
            self.download_button3.config(state='normal')

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label3.config(text="Error occurred", fg=self.warning_color)
        finally:
            self.predict_button.config(state='normal')

    def generate_predicted_emails(self):
        try:
            if self.df3 is None:
                raise ValueError("No prediction data available")

            df = self.df3.copy()
            df['client'] = df['First Name'] + ' ' + df['Last Name']

            def predict_email(row):
                try:
                    first_name = str(row['First Name']).lower().strip()
                    last_name = str(row['Last Name']).lower().strip()
                    format_type = str(row['Email Format'])
                    domain = str(row['Domain'])

                    if format_type == 'FirstName.LastName':
                        username = f"{first_name}.{last_name}"
                    elif format_type == 'FirstLetterLastName':
                        username = f"{first_name[0]}{last_name}"
                    elif format_type == 'LastName':
                        username = last_name
                    elif format_type == 'FirstName':
                        username = first_name
                    else:
                        username = f"{first_name}{last_name[0]}"

                    email = f"{username}@{domain}"
                    return email

                except Exception as e:
                    print(f"Error predicting email for row: {row}, Error: {str(e)}")
                    return "Error predicting email"

            df['Email generated'] = df.apply(predict_email, axis=1)
            self.processed_df3 = df
            return df

        except Exception as e:
            print(f"Error generating predicted emails: {str(e)}")
            messagebox.showerror("Error", f"Error generating predicted emails: {str(e)}")
            return None

    def setup_email_predictor_section(self, parent_frame):
        # Implement the Email Predictor section here
        upload_frame3 = tk.Frame(parent_frame, bg=self.bg_color)
        upload_frame3.pack(fill='x', pady=5)

        self.file_label3 = tk.Label(
            upload_frame3,
            text="No file selected",
            font=('Arial', 12),
            fg=self.warning_color,
            bg=self.bg_color
        )
        self.file_label3.pack(side='left', padx=10)

        self.upload_button3 = tk.Button(
            upload_frame3,
            text="Upload Predictor CSV",
            command=self.upload_file3,
            font=('Arial', 12, 'bold'),
            bg=self.accent_color,
            fg='white',
            padx=20,
            pady=5,
            cursor='hand2',
            relief='flat'
        )
        self.upload_button3.pack(side='right', padx=10)

        self.predict_button = tk.Button(
            upload_frame3,
            text="Predict Emails",
            command=self.predict_emails,
            state='disabled',
            font=('Arial', 12, 'bold'),
            bg=self.black,
            fg='white',
            padx=20,
            pady=5,
            cursor='hand2',
            relief='flat'
        )
        self.predict_button.pack(side='right', padx=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')]
        )
        if file_path:
            try:
                df = pd.read_csv(file_path)
                required_columns = ['Email', 'First Name', 'Last Name']

                if all(col in df.columns for col in required_columns):
                    self.df = df
                    self.file_label.config(
                        text=f"Selected: {os.path.basename(file_path)}",
                        fg=self.success_color
                    )
                    self.process_button.config(state='normal')
                else:
                    messagebox.showerror("Error", f"Missing required columns. Required: {', '.join(required_columns)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error reading file: {str(e)}")
                self.file_label.config(text="Error in file selection", fg=self.warning_color)

    def upload_file2(self):
        file_path = filedialog.askopenfilename(
            filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')]
        )
        if file_path:
            try:
                df = pd.read_csv(file_path)
                required_columns = ['First Name', 'Last Name', 'URL']

                if all(col in df.columns for col in required_columns):
                    self.df2 = df
                    self.file_label2.config(
                        text=f"Selected: {os.path.basename(file_path)}",
                        fg=self.success_color
                    )
                    self.process_button2.config(state='normal')
                else:
                    messagebox.showerror("Error", f"Missing required columns. Required: {', '.join(required_columns)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error reading file: {str(e)}")
                self.file_label2.config(text="Error in file selection", fg=self.warning_color)

    def process_file2(self):
        """Process the prediction file"""
        if self.df2 is None or not self.email_patterns:
            messagebox.showerror("Error", "Please process pattern file first!")
            return

        self.process_button2.config(state='disabled')
        threading.Thread(target=self._process_thread2, daemon=True).start()

    def _process_thread2(self):
        """Thread for processing prediction file"""
        try:
            self.status_label.config(text="Generating email addresses...")

            result_df = self.generate_emails()
            if result_df is not None:
                self.show_results(result_df)
                self.status_label.config(text="Email generation complete!", fg=self.success_color)
                self.download_button2.config(state='normal')

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="Error occurred", fg=self.warning_color)
        finally:
            self.process_button2.config(state='normal')

    def save_results3(self):
        if not hasattr(self, 'processed_df3') or self.processed_df3 is None:
            messagebox.showerror("Error", "No predictions to save. Please generate emails first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')],
            initialfile='email_predictions.csv'
        )

        if file_path:
            try:
                save_df = pd.DataFrame({
                    'First Name': self.processed_df3['First Name'],
                    'Last Name': self.processed_df3['Last Name'],
                    'Email Format': self.processed_df3['Email Format'],
                    'Domain': self.processed_df3['Domain'],
                    'Email generated': self.processed_df3['Email generated']
                })
                save_df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", "Email predictions saved successfully!")
            except Exception as e:
                print(f"Error saving predictions: {str(e)}")
                messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def generate_emails(self):
        try:
            if self.df2 is None:
                raise ValueError("No prediction data available")
            if not self.email_patterns:
                raise ValueError("No email patterns available. Please process pattern file first!")

            df = self.df2.copy()
            df['client'] = df['First Name'] + ' ' + df['Last Name']

            def clean_domain(url):
                try:
                    domain = str(url).lower().strip()
                    domain = domain.replace('http://', '').replace('https://', '').replace('www.', '')
                    return domain.split('/')[0]
                except:
                    return url

            def generate_email(row):
                try:
                    domain = clean_domain(row['URL'])
                    first_name = str(row['First Name']).lower().strip()
                    last_name = str(row['Last Name']).lower().strip()

                    # Get pattern for this domain
                    pattern = self.email_patterns.get(domain)
                    if not pattern:
                        for known_domain, known_pattern in self.email_patterns.items():
                            if known_domain in domain or domain in known_domain:
                                pattern = known_pattern
                                break

                    if not pattern:
                        pattern = 'FirstNameFirstLetterLastName'  # Default pattern

                    # Generate username based on pattern
                    if pattern == 'LastNameFirstLetterFirstName':  # For djoe case
                        username = f"d{first_name}"
                    elif pattern == 'FirstNameFirstLetterLastName':  # For ashleyj, fernandof, lisaa cases
                        username = f"{first_name}{last_name[0]}"
                    elif pattern == 'FirstNameLastName':  # For willcom case
                        username = f"{first_name}{last_name}"
                    elif pattern == 'FirstLetterLastName':
                        username = f"{first_name[0]}{last_name}"
                    elif pattern == 'FirstName.LastName':
                        username = f"{first_name}.{last_name}"
                    elif pattern == 'FirstName_LastName':
                        username = f"{first_name}_{last_name}"
                    elif pattern == 'LastName':
                        username = last_name
                    elif pattern == 'FirstName':
                        username = first_name
                    else:
                        username = f"{first_name}{last_name[0]}"  # Default format

                    email = f"{username}@{domain}"
                    display_format = f"{pattern}@{domain}"
                    print(f"Generated {email} using pattern {pattern}")
                    return email, display_format

                except Exception as e:
                    print(f"Error generating email for row: {row}, Error: {str(e)}")
                    return "Error generating email", "error"

            # Generate emails and formats
            emails_and_formats = [generate_email(row) for _, row in df.iterrows()]
            df['predicted_email'] = [e[0] for e in emails_and_formats]
            df['format'] = [e[1] for e in emails_and_formats]

            self.processed_df2 = df
            return df

        except Exception as e:
            print(f"Error generating emails: {str(e)}")
            messagebox.showerror("Error", f"Error generating emails: {str(e)}")
            return None

    def save_results(self):
        if not hasattr(self, 'processed_df') or self.processed_df is None:
            messagebox.showerror("Error", "No results to save. Please process the data first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')],
            initialfile='pattern_analysis_results.csv'
        )

        if file_path:
            try:
                save_df = pd.DataFrame({
                    'Client': self.processed_df['client'],
                    'Domain': self.processed_df['domain'],
                    'Email Format': self.processed_df['format'],  # Now includes domain
                    'Email': self.processed_df['Email']
                })
                save_df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", "Pattern analysis results saved successfully!")
            except Exception as e:
                print(f"Error saving results: {str(e)}")
                messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def save_results2(self):
        if not hasattr(self, 'processed_df2') or self.processed_df2 is None:
            messagebox.showerror("Error", "No predictions to save. Please generate emails first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')],
            initialfile='email_predictions.csv'
        )

        if file_path:
            try:
                save_df = pd.DataFrame({
                    'Client': self.processed_df2['client'],
                    'Domain': self.processed_df2['URL'],
                    'Email Format': self.processed_df2['format'],  # Now includes domain
                    'Predicted Email': self.processed_df2['predicted_email']
                })
                save_df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", "Email predictions saved successfully!")
            except Exception as e:
                print(f"Error saving predictions: {str(e)}")
                messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def process_file(self):
        if self.df is None:
            return
        self.process_button.config(state='disabled')
        threading.Thread(target=self._process_thread, daemon=True).start()


    def _process_thread(self):
        try:
            self.progress_bar['value'] = 20
            self.status_label.config(text="Processing patterns...")

            result_df = self.process_data()
            if result_df is not None:
                self.progress_bar['value'] = 70
                self.status_label.config(text="Updating preview...")

                self.update_results(result_df)

                self.progress_bar['value'] = 100
                self.status_label.config(text="Processing complete!", fg=self.success_color)
                self.download_button.config(state='normal')

        except Exception as e:
            print(f"Error in processing: {str(e)}")
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="Error occurred", fg=self.warning_color)
        finally:
            self.process_button.config(state='normal')

    def process_data(self):
        try:
            if self.df is None:
                raise ValueError("No data available")

            df = self.df.copy()
            df['client'] = df['First Name'] + ' ' + df['Last Name']

            def analyze_email(row):
                try:
                    email = str(row['Email']).lower()
                    domain = email.split('@')[1]
                    username = email.split('@')[0]
                    first_name = str(row['First Name']).lower().strip()
                    last_name = str(row['Last Name']).lower().strip()

                    # Print debug information
                    print(f"\nAnalyzing email: {email}")
                    print(f"First Name: {first_name}")
                    print(f"Last Name: {last_name}")
                    print(f"Username: {username}")

                    # Enhanced pattern detection with more specific cases
                    if username == f"d{first_name}":  # djoe
                        format_type = 'LastNameFirstLetterFirstName'
                    elif username == f"{first_name}{first_name[0]}":  # fernandof
                        format_type = 'FirstNameFirstLetterLastName'
                    elif username == f"{first_name}{last_name[0]}":  # ashleyj
                        format_type = 'FirstNameFirstLetterLastName'
                    elif username == f"{first_name}{last_name}":  # willcom
                        format_type = 'FirstNameLastName'
                    elif username == f"{first_name}{last_name[0]}":  # lisaa
                        format_type = 'FirstNameFirstLetterLastName'
                    elif username == f"{first_name[0]}{last_name}":
                        format_type = 'FirstLetterLastName'
                    elif username == f"{first_name}.{last_name}":
                        format_type = 'FirstName.LastName'
                    elif username == f"{first_name}_{last_name}":
                        format_type = 'FirstName_LastName'
                    elif username == last_name:
                        format_type = 'LastName'
                    elif username == first_name:
                        format_type = 'FirstName'
                    else:
                        # Additional pattern checks
                        if username.startswith(first_name.lower()):
                            format_type = 'FirstNameFirstLetterLastName'
                        elif username.startswith('d'):
                            format_type = 'LastNameFirstLetterFirstName'
                        else:
                            print(f"Unrecognized pattern for: {email}")
                            format_type = 'FirstNameFirstLetterLastName'  # Default pattern

                    # Add domain to format
                    format_with_domain = f"{format_type}@{domain}"
                    print(f"Detected format: {format_with_domain}")
                    return domain, format_with_domain

                except Exception as e:
                    print(f"Error analyzing email: {str(e)}")
                    return None, 'invalid'

            df[['domain', 'format']] = pd.DataFrame(df.apply(analyze_email, axis=1).tolist(), index=df.index)

            # Store patterns by domain
            self.email_patterns = {}
            for _, row in df.iterrows():
                if pd.notna(row['domain']):
                    pattern = row['format'].split('@')[0]  # Remove domain part for storage
                    self.email_patterns[row['domain']] = pattern
                    print(f"Stored pattern for {row['domain']}: {pattern}")

            self.processed_df = df
            return df

        except Exception as e:
            print(f"Error in process_data: {str(e)}")
            messagebox.showerror("Error", f"Error processing data: {str(e)}")
            return None

    def update_results(self, df):
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert new data
            for _, row in df.iterrows():
                values = (
                    row['client'],
                    row.get('domain', ''),
                    row.get('format', ''),
                    row['Email']
                )
                self.tree.insert('', 'end', values=values)

        except Exception as e:
            print(f"Error updating results: {str(e)}")
            messagebox.showerror("Error", f"Error showing results: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TreeBusinessGUI()
    app.run()