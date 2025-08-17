from jobtracker.resume.parser import resume_parser

if __name__ == "__main__":
    # Replace with your actual resume path
    resume_path = "../sample_resume.pdf"
    profile = resume_parser(resume_path)
    print("Extracted Resume Profile:")
    print(profile)
